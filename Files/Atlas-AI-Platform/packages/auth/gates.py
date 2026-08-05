"""Feature gates for tenant-aware AI behavior.

Until tenant membership and RBAC tables exist, sensitive tenant-scoped features
must call this guard. It fails closed unless the caller proves both membership
and RBAC readiness through explicit permission markers.
"""

from collections.abc import Collection

from packages.core.errors import PermissionDeniedError

TENANT_RBAC_REQUIRED_BEFORE: frozenset[str] = frozenset(
    {
        "model_gateway.tenant_route",
        "rag.collection",
        "evals.tenant_run",
        "tools.mcp_tool",
        "agents.action",
    }
)


def enforce_tenant_rbac_gate(
    feature_key: str,
    granted_permissions: Collection[str],
) -> None:
    """Raise PermissionDeniedError if a gated feature is used too early."""
    if feature_key not in TENANT_RBAC_REQUIRED_BEFORE:
        return

    # These permission strings are temporary phase gates, not the final RBAC
    # implementation. They force future work to make the security dependency
    # explicit before enabling tenant-scoped AI actions.
    has_membership = "tenant.membership.verified" in granted_permissions
    has_rbac = "tenant.rbac.ready" in granted_permissions
    if has_membership and has_rbac:
        return

    raise PermissionDeniedError(
        message=(
            "Tenant membership and RBAC must be implemented before this tenant-aware "
            "AI feature can run."
        ),
        details={"feature_key": feature_key, "required_gate": "tenant_rbac"},
    )
