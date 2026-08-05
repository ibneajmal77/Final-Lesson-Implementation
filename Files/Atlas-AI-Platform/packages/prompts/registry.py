"""Prompt resolution and short-lived active-version cache.

The registry answers "which prompt version should this use case run with?" and
can render it immediately. It prefers tenant-specific active prompts, falls back
to global prompts, and supports pinned version ids for reproducible test runs.
"""

from __future__ import annotations

import time
from dataclasses import dataclass
from typing import ClassVar
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from packages.db.models.prompts import PromptTemplate, PromptVersion
from packages.prompts.contracts import (
    PromptResolution,
    RenderedPrompt,
    ResolvedPromptVersion,
)
from packages.prompts.errors import PromptNotFoundError, no_active_version_error
from packages.prompts.records import version_spec_from_models
from packages.prompts.renderer import render_prompt


@dataclass(frozen=True, slots=True)
class _CachedVersion:
    expires_at: float
    resolved: ResolvedPromptVersion


class PromptRegistry:
    """Resolve active or pinned prompt versions."""

    # Class variables are shared by every PromptRegistry instance in the process.
    # This is intentional for a lightweight active-prompt cache.
    _cache: ClassVar[dict[tuple[str | None, str], _CachedVersion]] = {}

    def __init__(self, session: Session, *, ttl_seconds: int = 30) -> None:
        self._session = session
        self._ttl_seconds = ttl_seconds

    def resolve(
        self,
        *,
        tenant_id: UUID | None,
        use_case: str,
        prompt_version_id: UUID | None = None,
    ) -> ResolvedPromptVersion:
        if prompt_version_id is not None:
            # Pinned resolution bypasses the active-version cache so historical
            # or test runs always use the exact requested version.
            return self._resolve_pinned(prompt_version_id)

        cache_key = _cache_key(tenant_id, use_case)
        cached = self._cache.get(cache_key)
        now = time.monotonic()
        if cached is not None and cached.expires_at > now:
            return ResolvedPromptVersion(
                version=cached.resolved.version,
                resolution=cached.resolved.resolution,
                cache_hit=True,
            )

        resolved = self._resolve_active(tenant_id=tenant_id, use_case=use_case)
        self._cache[cache_key] = _CachedVersion(
            expires_at=now + self._ttl_seconds,
            resolved=resolved,
        )
        return resolved

    def render(
        self,
        *,
        tenant_id: UUID | None,
        use_case: str,
        variables: dict[str, object],
        prompt_version_id: UUID | None = None,
    ) -> RenderedPrompt:
        resolved = self.resolve(
            tenant_id=tenant_id,
            use_case=use_case,
            prompt_version_id=prompt_version_id,
        )
        return render_prompt(resolved, variables)

    @classmethod
    def invalidate(cls, *, tenant_id: UUID | None, use_case: str) -> None:
        cls._cache.pop(_cache_key(tenant_id, use_case), None)

    @classmethod
    def clear_cache(cls) -> None:
        cls._cache.clear()

    def _resolve_pinned(self, prompt_version_id: UUID) -> ResolvedPromptVersion:
        row = self._session.execute(
            select(PromptVersion, PromptTemplate)
            .join(PromptTemplate, PromptVersion.prompt_template_id == PromptTemplate.id)
            .where(PromptVersion.id == prompt_version_id)
        ).one_or_none()
        if row is None:
            raise PromptNotFoundError(
                code="prompts.version_not_found",
                message="Prompt version not found.",
                details={"prompt_version_id": str(prompt_version_id)},
            )
        version, template = row
        return ResolvedPromptVersion(
            version=version_spec_from_models(version=version, template=template),
            resolution="pinned",
            cache_hit=False,
        )

    def _resolve_active(
        self,
        *,
        tenant_id: UUID | None,
        use_case: str,
    ) -> ResolvedPromptVersion:
        if tenant_id is not None:
            # Tenant prompts override global prompts, matching common SaaS
            # configuration precedence.
            tenant_version = self._select_active(tenant_id=tenant_id, use_case=use_case)
            if tenant_version is not None:
                return _resolved_from_row(tenant_version, resolution="tenant")

        global_version = self._select_active(tenant_id=None, use_case=use_case)
        if global_version is not None:
            return _resolved_from_row(global_version, resolution="global")

        raise no_active_version_error(tenant_id=tenant_id, use_case=use_case)

    def _select_active(
        self,
        *,
        tenant_id: UUID | None,
        use_case: str,
    ) -> tuple[PromptVersion, PromptTemplate] | None:
        row = self._session.execute(
            select(PromptVersion, PromptTemplate)
            .join(PromptTemplate, PromptVersion.prompt_template_id == PromptTemplate.id)
            .where(
                PromptTemplate.tenant_id.is_(None)
                if tenant_id is None
                else PromptTemplate.tenant_id == tenant_id,
                PromptTemplate.use_case == use_case,
                PromptTemplate.status == "active",
                PromptVersion.status == "active",
            )
            .order_by(PromptTemplate.created_at.desc(), PromptVersion.version_number.desc())
            .limit(1)
        ).first()
        if row is None:
            return None
        version, template = row
        return version, template


def _resolved_from_row(
    row: tuple[PromptVersion, PromptTemplate],
    *,
    resolution: PromptResolution,
) -> ResolvedPromptVersion:
    version, template = row
    return ResolvedPromptVersion(
        version=version_spec_from_models(version=version, template=template),
        resolution=resolution,
        cache_hit=False,
    )


def _cache_key(tenant_id: UUID | None, use_case: str) -> tuple[str | None, str]:
    """Use strings in the cache key so UUID object identity never matters."""
    return (str(tenant_id) if tenant_id is not None else None, use_case)
