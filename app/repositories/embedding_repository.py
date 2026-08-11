"""Database queries for retrieving stored embeddings."""

from sqlalchemy import select

from app.core.config import settings
from app.db.engine import engine
from app.db.tables import courses, embeddings, skills


def get_skill_embeddings(skill_names):
    """Retrieve stored vectors for a list of standardized skills."""

    if not skill_names:
        return []

    statement = (
        select(
            skills.c.id.label("skill_id"),
            skills.c.name.label("skill_name"),
            embeddings.c.vector,
            embeddings.c.dimensions,
            embeddings.c.model_name,
        )
        .select_from(
            skills.join(
                embeddings,
                (
                    embeddings.c.entity_id == skills.c.id
                )
                & (
                    embeddings.c.entity_type == "skill"
                ),
            )
        )
        .where(skills.c.name.in_(skill_names))
        .where(
            embeddings.c.model_name
            == settings.embedding_model
        )
        .order_by(skills.c.name)
    )

    with engine.connect() as connection:
        rows = connection.execute(
            statement
        ).mappings().all()

    return [
        dict(row)
        for row in rows
    ]


def get_courses_with_embeddings():
    """Retrieve courses together with their stored vectors."""

    statement = (
        select(
            courses.c.id.label("course_id"),
            courses.c.title,
            courses.c.description,
            courses.c.skills,
            embeddings.c.vector,
            embeddings.c.dimensions,
            embeddings.c.model_name,
        )
        .select_from(
            courses.join(
                embeddings,
                (
                    embeddings.c.entity_id == courses.c.id
                )
                & (
                    embeddings.c.entity_type == "course"
                ),
            )
        )
        .where(
            embeddings.c.model_name
            == settings.embedding_model
        )
        .order_by(courses.c.id)
    )

    with engine.connect() as connection:
        rows = connection.execute(
            statement
        ).mappings().all()

    return [
        dict(row)
        for row in rows
    ]