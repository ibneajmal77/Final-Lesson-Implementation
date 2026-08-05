"""Import all ORM models so Alembic can see the complete metadata graph.

This mirrors making sure every EF entity type is registered with the DbContext
before running migrations or schema comparisons.
"""

from packages.db.models.audit import AuditEvent
from packages.db.models.identity import Tenant, User
from packages.db.models.model_gateway import AIRun, CostRecord, ModelProvider, ModelRoute
from packages.db.models.prompts import PromptTemplate, PromptTestCase, PromptVersion

__all__ = [
    "AIRun",
    "AuditEvent",
    "CostRecord",
    "ModelProvider",
    "ModelRoute",
    "PromptTemplate",
    "PromptTestCase",
    "PromptVersion",
    "Tenant",
    "User",
]
