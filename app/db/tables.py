"""SQLAlchemy Core table definitions."""

from sqlalchemy import (
    CheckConstraint,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    MetaData,
    String,
    Table,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB


metadata = MetaData()


users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(100), nullable=False),
    Column("email", String(255), nullable=False, unique=True),
    Column(
        "created_at",
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    ),
)


skills = Table(
    "skills",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(100), nullable=False, unique=True),
    Column(
        "created_at",
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    ),
)


courses = Table(
    "courses",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String(255), nullable=False, unique=True),
    Column("description", Text, nullable=False),
    Column("skills", JSONB, nullable=False, server_default="[]"),
    Column(
        "created_at",
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    ),
)


user_skills = Table(
    "user_skills",
    metadata,
    Column(
        "user_id",
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "skill_id",
        Integer,
        ForeignKey("skills.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "created_at",
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    ),
)


embeddings = Table(
    "embeddings",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("entity_type", String(20), nullable=False),
    Column("entity_id", Integer, nullable=False),
    Column("model_name", String(255), nullable=False),
    Column("vector", JSONB, nullable=False),
    Column("dimensions", Integer, nullable=False),
    Column(
        "created_at",
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    ),
    CheckConstraint(
        "entity_type IN ('skill', 'course')",
        name="ck_embeddings_entity_type",
    ),
    CheckConstraint(
        "dimensions > 0",
        name="ck_embeddings_dimensions_positive",
    ),
    UniqueConstraint(
        "entity_type",
        "entity_id",
        "model_name",
        name="uq_embeddings_entity_model",
    ),
)


recommendation_logs = Table(
    "recommendation_logs",
    metadata,
    Column("id", Integer, primary_key=True),
    Column(
        "user_id",
        Integer,
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    ),
    Column("input_text", Text, nullable=True),
    Column("extracted_skills", JSONB, nullable=False),
    Column("recommended_courses", JSONB, nullable=False),
    Column("top_n", Integer, nullable=False),
    Column("status", String(30), nullable=False),
    Column("error_message", Text, nullable=True),
    Column("processing_time_ms", Float, nullable=True),
    Column(
        "created_at",
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    ),
    CheckConstraint(
        "top_n > 0",
        name="ck_recommendation_logs_top_n_positive",
    ),
)