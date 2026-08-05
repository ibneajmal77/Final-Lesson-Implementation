"""Unit tests for temporary tenant/RBAC rollout gates."""

import pytest

from packages.auth.gates import TENANT_RBAC_REQUIRED_BEFORE, enforce_tenant_rbac_gate
from packages.core.errors import PermissionDeniedError


def test_tenant_rbac_gate_blocks_tenant_aware_ai_features_before_rbac() -> None:
    with pytest.raises(PermissionDeniedError) as exc_info:
        enforce_tenant_rbac_gate("rag.collection", granted_permissions=[])

    assert exc_info.value.code == "permission_denied"
    assert exc_info.value.details == {
        "feature_key": "rag.collection",
        "required_gate": "tenant_rbac",
    }


def test_tenant_rbac_gate_allows_feature_after_membership_and_rbac_are_ready() -> None:
    enforce_tenant_rbac_gate(
        "agents.action",
        granted_permissions={"tenant.membership.verified", "tenant.rbac.ready"},
    )


def test_tenant_rbac_gate_does_not_block_non_tenant_features() -> None:
    enforce_tenant_rbac_gate("health.check", granted_permissions=[])


def test_tenant_rbac_gate_lists_all_phase_critical_features() -> None:
    assert TENANT_RBAC_REQUIRED_BEFORE == frozenset(
        {
            "model_gateway.tenant_route",
            "rag.collection",
            "evals.tenant_run",
            "tools.mcp_tool",
            "agents.action",
        }
    )
