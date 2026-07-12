from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker


def to_sqlalchemy_url(database_url: str) -> str:
    if database_url.startswith("postgresql://"):
        return database_url.replace("postgresql://", "postgresql+psycopg://", 1)
    return database_url


def create_db_engine(database_url: str) -> Engine:
    return create_engine(to_sqlalchemy_url(database_url), pool_pre_ping=True)


def create_session_factory(engine: Engine) -> sessionmaker[Session]:
    return sessionmaker(bind=engine, autoflush=False, autocommit=False)
