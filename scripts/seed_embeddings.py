"""Generate and store skill and course embeddings."""

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert

from app.core.config import settings
from app.db.engine import engine
from app.db.tables import courses, embeddings, skills
from app.services.embedding_service import generate_embeddings


def build_course_text(course):
    """Combine course fields into one text value."""

    skills_text = ", ".join(course["skills"])

    return (
        f"Course title: {course['title']}. "
        f"Description: {course['description']} "
        f"Skills taught: {skills_text}."
    )


def save_embedding(
    connection,
    entity_type,
    entity_id,
    vector,
):
    """Insert or update one embedding record."""

    vector_list = vector.tolist()

    statement = insert(embeddings).values(
        entity_type=entity_type,
        entity_id=entity_id,
        model_name=settings.embedding_model,
        vector=vector_list,
        dimensions=len(vector_list),
    )

    statement = statement.on_conflict_do_update(
        constraint="uq_embeddings_entity_model",
        set_={
            "vector": vector_list,
            "dimensions": len(vector_list),
        },
    )

    connection.execute(statement)


def seed_skill_embeddings(connection):
    """Generate and store embeddings for all skills."""

    print("Loading skills from PostgreSQL...")

    skill_rows = connection.execute(
        select(
            skills.c.id,
            skills.c.name,
        ).order_by(skills.c.id)
    ).mappings().all()

    if not skill_rows:
        print("No skills were found.")
        return

    skill_names = [
        row["name"]
        for row in skill_rows
    ]

    print(
        f"Generating embeddings for "
        f"{len(skill_names)} skills..."
    )

    skill_vectors = generate_embeddings(skill_names)

    for skill, vector in zip(
        skill_rows,
        skill_vectors,
        strict=True,
    ):
        save_embedding(
            connection=connection,
            entity_type="skill",
            entity_id=skill["id"],
            vector=vector,
        )

    print(
        f"Stored {len(skill_rows)} skill embeddings."
    )


def seed_course_embeddings(connection):
    """Generate and store embeddings for all courses."""

    print("Loading courses from PostgreSQL...")

    course_rows = connection.execute(
        select(
            courses.c.id,
            courses.c.title,
            courses.c.description,
            courses.c.skills,
        ).order_by(courses.c.id)
    ).mappings().all()

    if not course_rows:
        print("No courses were found.")
        return

    course_texts = [
        build_course_text(course)
        for course in course_rows
    ]

    print(
        f"Generating embeddings for "
        f"{len(course_texts)} courses..."
    )

    course_vectors = generate_embeddings(course_texts)

    for course, vector in zip(
        course_rows,
        course_vectors,
        strict=True,
    ):
        save_embedding(
            connection=connection,
            entity_type="course",
            entity_id=course["id"],
            vector=vector,
        )

    print(
        f"Stored {len(course_rows)} course embeddings."
    )


def main():
    """Generate all database embeddings."""

    print("Starting embedding seed...")

    with engine.begin() as connection:
        seed_skill_embeddings(connection)
        seed_course_embeddings(connection)

    print("Embedding seed completed successfully.")


if __name__ == "__main__":
    main()