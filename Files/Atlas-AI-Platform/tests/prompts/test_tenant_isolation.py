"""Tenant isolation tests for the prompt system.

This file was planned in Phase 01, Phase 02, and Phase 03 and written in none of
them, which left the single most security-relevant property of a multi-tenant
prompt store completely unasserted: that one tenant's prompt never reaches
another tenant.

Two distinct boundaries are covered, because they fail differently:

1. Resolution — `PromptRegistry` must never return tenant B's active version to
   tenant A, and must fall through to the global prompt instead.
2. Direct access by id — knowing a template id must not be enough to read it.
"""

from __future__ import annotations

import pytest
from sqlalchemy.orm import Session

from packages.db.models.identity import Tenant
from packages.prompts.contracts import VariableDeclaration
from packages.prompts.errors import PromptNotFoundError
from packages.prompts.registry import PromptRegistry
from packages.prompts.service import PromptService


@pytest.fixture()
def other_tenant(db_session: Session) -> Tenant:
    """A second tenant, so isolation has two real sides to test."""
    from uuid import uuid4

    suffix = uuid4().hex
    tenant = Tenant(name=f"Other Tenant {suffix}", slug=f"other-tenant-{suffix}")
    db_session.add(tenant)
    db_session.commit()
    db_session.refresh(tenant)
    return tenant


def _activate_template(
    service: PromptService,
    *,
    tenant_id,
    name: str,
    system_prompt: str,
    use_case: str = "chat",
):
    """Create, approve, and activate a prompt version in one step."""
    template = service.create_template(tenant_id=tenant_id, name=name, use_case=use_case)
    version = service.create_version(
        template_id=template.id,
        system_prompt=system_prompt,
        user_template="${question}",
        input_variables=(VariableDeclaration(name="question", required=True, trusted=False),),
    )
    service.approve_version(template_id=template.id, version_id=version.id, actor_user_id=None)
    service.activate_version(
        template_id=template.id,
        version_id=version.id,
        actor_user_id=None,
        reason="isolation test setup",
    )
    return template, version


def test_tenant_prompt_does_not_leak_into_another_tenant_resolution(
    db_session: Session,
    tenant: Tenant,
    other_tenant: Tenant,
) -> None:
    service = PromptService(db_session)
    _activate_template(
        service,
        tenant_id=tenant.id,
        name=f"isolation_a_{tenant.slug}",
        system_prompt="TENANT A SECRET PROMPT",
    )
    _activate_template(
        service,
        tenant_id=other_tenant.id,
        name=f"isolation_b_{other_tenant.slug}",
        system_prompt="TENANT B SECRET PROMPT",
    )
    PromptRegistry.clear_cache()

    resolved_a = PromptRegistry(db_session).resolve(tenant_id=tenant.id, use_case="chat")
    resolved_b = PromptRegistry(db_session).resolve(tenant_id=other_tenant.id, use_case="chat")

    assert resolved_a.version.system_prompt == "TENANT A SECRET PROMPT"
    assert resolved_b.version.system_prompt == "TENANT B SECRET PROMPT"
    assert resolved_a.version.tenant_id == tenant.id
    assert resolved_b.version.tenant_id == other_tenant.id
    assert resolved_a.version.id != resolved_b.version.id


def test_registry_cache_is_keyed_by_tenant(
    db_session: Session,
    tenant: Tenant,
    other_tenant: Tenant,
) -> None:
    """A cache shared across tenants would be the cheapest possible leak.

    The first tenant's resolution populates the cache; the second must not read
    that entry. This is asserted separately from plain resolution because a
    tenant-blind cache key would still pass the test above on a cold cache.
    """
    service = PromptService(db_session)
    _activate_template(
        service,
        tenant_id=tenant.id,
        name=f"isolation_cache_a_{tenant.slug}",
        system_prompt="CACHE TENANT A",
    )
    _activate_template(
        service,
        tenant_id=other_tenant.id,
        name=f"isolation_cache_b_{other_tenant.slug}",
        system_prompt="CACHE TENANT B",
    )
    PromptRegistry.clear_cache()

    registry = PromptRegistry(db_session)
    first = registry.resolve(tenant_id=tenant.id, use_case="chat")
    second = registry.resolve(tenant_id=other_tenant.id, use_case="chat")
    # Re-resolving the first tenant should now be a cache hit, still with its
    # own prompt rather than whatever the second lookup stored.
    first_again = registry.resolve(tenant_id=tenant.id, use_case="chat")

    assert first.cache_hit is False
    assert second.cache_hit is False
    assert first_again.cache_hit is True
    assert second.version.system_prompt == "CACHE TENANT B"
    assert first_again.version.system_prompt == "CACHE TENANT A"


def test_tenant_without_own_prompt_falls_through_to_global_not_to_a_peer(
    db_session: Session,
    tenant: Tenant,
    other_tenant: Tenant,
) -> None:
    service = PromptService(db_session)
    _activate_template(
        service,
        tenant_id=other_tenant.id,
        name=f"isolation_peer_{other_tenant.slug}",
        system_prompt="PEER TENANT PROMPT",
        use_case="llm_judge",
    )
    _activate_template(
        service,
        tenant_id=None,
        name=f"isolation_global_{other_tenant.slug}",
        system_prompt="GLOBAL PROMPT",
        use_case="llm_judge",
    )
    PromptRegistry.clear_cache()

    resolved = PromptRegistry(db_session).resolve(tenant_id=tenant.id, use_case="llm_judge")

    assert resolved.resolution == "global"
    assert resolved.version.system_prompt == "GLOBAL PROMPT"


def test_reading_a_template_by_id_is_refused_across_tenants(
    db_session: Session,
    tenant: Tenant,
    other_tenant: Tenant,
) -> None:
    """Knowing the id must not be enough to read another tenant's template."""
    service = PromptService(db_session)
    template, _ = _activate_template(
        service,
        tenant_id=other_tenant.id,
        name=f"isolation_byid_{other_tenant.slug}",
        system_prompt="BY ID SECRET",
    )

    with pytest.raises(PromptNotFoundError) as exc_info:
        service.get_template(template.id, tenant_scope=tenant.id)

    # 404, not 403: a "forbidden" response would confirm the id is real and let
    # an attacker enumerate another tenant's templates.
    assert exc_info.value.status_code == 404
    assert exc_info.value.code == "prompts.template_not_found"


def test_global_templates_stay_readable_by_every_tenant(
    db_session: Session,
    tenant: Tenant,
) -> None:
    """Scoping must not break the global-prompt case it shares a code path with."""
    service = PromptService(db_session)
    template, _ = _activate_template(
        service,
        tenant_id=None,
        name=f"isolation_global_read_{tenant.slug}",
        system_prompt="SHARED GLOBAL",
        use_case="classification",
    )

    loaded = service.get_template(template.id, tenant_scope=tenant.id)

    assert loaded.id == template.id
    assert loaded.tenant_id is None


def test_listing_templates_for_a_tenant_excludes_other_tenants(
    db_session: Session,
    tenant: Tenant,
    other_tenant: Tenant,
) -> None:
    service = PromptService(db_session)
    _activate_template(
        service,
        tenant_id=tenant.id,
        name=f"isolation_list_a_{tenant.slug}",
        system_prompt="LIST A",
    )
    _activate_template(
        service,
        tenant_id=other_tenant.id,
        name=f"isolation_list_b_{other_tenant.slug}",
        system_prompt="LIST B",
    )

    listed = service.list_templates(tenant_id=tenant.id)

    assert listed, "the tenant's own template should be listed"
    assert {template.tenant_id for template in listed} == {tenant.id}
