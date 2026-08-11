"""Database queries related to courses."""

from sqlalchemy import select

from app.db.engine import engine
from app.db.tables import courses, embeddings


def get_all_courses():
    """Return all courses."""

    statement = (
        select(
            courses.c.id,
            courses.c.title,
            courses.c.description,
            courses.c.skills,
        )
        .order_by(courses.c.id)
    )

    with engine.connect() as connection:
        rows = connection.execute(
            statement
        ).mappings().all()

    return [dict(row) for row in rows]


def get_course_embeddings():
    """Return all stored course embeddings."""

    statement = (
        select(
            embeddings.c.entity_id,
            embeddings.c.vector,
        )
        .where(
            embeddings.c.entity_type == "course"
        )
    )

    with engine.connect() as connection:
        rows = connection.execute(
            statement
        ).mappings().all()

    return [dict(row) for row in rows]