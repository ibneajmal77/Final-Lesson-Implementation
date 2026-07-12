from sqlalchemy import UniqueConstraint

from supportops_db.models import (
    Base,
    RecommendationReview,
    Tenant,
    Ticket,
    TicketRecommendation,
    User,
)
from supportops_db.session import to_sqlalchemy_url


def test_core_tables_are_registered() -> None:
    assert set(Base.metadata.tables) >= {
        "tenants",
        "users",
        "tickets",
        "ticket_recommendations",
        "recommendation_reviews",
    }


def test_tenant_table_columns() -> None:
    columns = Tenant.__table__.columns

    assert "id" in columns
    assert "name" in columns
    assert "slug" in columns
    assert "created_at" in columns


def test_user_table_has_tenant_email_unique_constraint() -> None:
    constraints = {
        constraint.name
        for constraint in User.__table__.constraints
        if isinstance(constraint, UniqueConstraint)
    }

    assert "uq_users_tenant_email" in constraints


def test_ticket_table_has_tenant_external_id_unique_constraint() -> None:
    constraints = {
        constraint.name
        for constraint in Ticket.__table__.constraints
        if isinstance(constraint, UniqueConstraint)
    }

    assert "uq_tickets_tenant_external_id" in constraints


def test_ticket_recommendation_table_has_tenant_and_ticket_indexes() -> None:
    index_names = {index.name for index in TicketRecommendation.__table__.indexes}

    assert "ix_ticket_recommendations_tenant_id" in index_names
    assert "ix_ticket_recommendations_ticket_id" in index_names
    assert "ix_ticket_recommendations_tenant_ticket" in index_names


def test_ticket_recommendation_table_has_model_output_columns() -> None:
    columns = TicketRecommendation.__table__.columns

    assert "model_name" in columns
    assert "prompt_version" in columns
    assert "summary" in columns
    assert "suggested_reply" in columns


def test_recommendation_review_table_has_audit_columns_and_indexes() -> None:
    columns = RecommendationReview.__table__.columns
    index_names = {index.name for index in RecommendationReview.__table__.indexes}

    assert "reviewer_user_id" in columns
    assert "decision" in columns
    assert "final_summary" in columns
    assert "final_reply" in columns
    assert "notes" in columns
    assert "ix_recommendation_reviews_recommendation_id" in index_names
    assert "ix_recommendation_reviews_tenant_ticket" in index_names


def test_database_url_is_converted_for_sqlalchemy_psycopg_driver() -> None:
    url = "postgresql://supportops:supportops@postgres:5432/supportops"

    assert (
        to_sqlalchemy_url(url)
        == "postgresql+psycopg://supportops:supportops@postgres:5432/supportops"
    )


def test_non_postgres_url_is_not_changed() -> None:
    url = "sqlite:///local.db"

    assert to_sqlalchemy_url(url) == url
