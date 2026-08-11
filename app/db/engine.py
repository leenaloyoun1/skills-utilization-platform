"""SQLAlchemy Core PostgreSQL engine."""

from sqlalchemy import Engine, create_engine

from app.core.config import settings


def create_database_engine() -> Engine:
    return create_engine(
        settings.database_url,
        echo=settings.debug,
        pool_pre_ping=True,
    )


engine = create_database_engine()