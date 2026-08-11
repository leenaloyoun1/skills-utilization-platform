"""Insert sample data into PostgreSQL using SQLAlchemy Core."""

import json
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert

from app.db.engine import engine
from app.db.tables import courses, skills, user_skills, users


COURSES_FILE = Path("data/courses.json")


STANDARD_SKILLS = [
    "Artificial Intelligence",
    "Machine Learning",
    "Deep Learning",
    "Natural Language Processing",
    "Data Science",
    "Data Analysis",
    "Python",
    "SQL",
    "Database Design",
    "Backend Development",
    "API Development",
    "FastAPI",
    "Git",
    "GitHub",
    "Cloud Computing",
    "Docker",
]


SAMPLE_USERS = [
    {
        "name": "Leen",
        "email": "leen@example.com",
        "skills": [
            "Python",
            "SQL",
            "Backend Development",
        ],
    },
    {
        "name": "AI Learner",
        "email": "ai.learner@example.com",
        "skills": [
            "Artificial Intelligence",
            "Machine Learning",
            "Natural Language Processing",
        ],
    },
    {
        "name": "Database Learner",
        "email": "database.learner@example.com",
        "skills": [
            "SQL",
            "Database Design",
        ],
    },
]


def load_courses():
    """Load sample course data from the JSON file."""

    with COURSES_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def seed_skills(connection):
    """Insert standardized skills without duplicates."""

    print("Seeding skills...")

    for skill_name in STANDARD_SKILLS:
        statement = insert(skills).values(
            name=skill_name,
        )

        statement = statement.on_conflict_do_nothing(
            index_elements=[skills.c.name],
        )

        connection.execute(statement)


def seed_courses(connection):
    """Insert or update courses from the JSON file."""

    print("Seeding courses...")

    course_data = load_courses()

    for course in course_data:
        statement = insert(courses).values(
            id=course["id"],
            title=course["title"],
            description=course["description"],
            skills=course["skills"],
        )

        statement = statement.on_conflict_do_update(
            index_elements=[courses.c.title],
            set_={
                "description": course["description"],
                "skills": course["skills"],
            },
        )

        connection.execute(statement)


def seed_users(connection):
    """Insert or update sample users."""

    print("Seeding users...")

    for user in SAMPLE_USERS:
        statement = insert(users).values(
            name=user["name"],
            email=user["email"],
        )

        statement = statement.on_conflict_do_update(
            index_elements=[users.c.email],
            set_={
                "name": user["name"],
            },
        )

        connection.execute(statement)


def seed_user_skills(connection):
    """Connect users with their standardized skills."""

    print("Seeding user-skill relationships...")

    user_rows = connection.execute(
        select(
            users.c.id,
            users.c.email,
        )
    ).mappings().all()

    skill_rows = connection.execute(
        select(
            skills.c.id,
            skills.c.name,
        )
    ).mappings().all()

    user_ids = {
        row["email"]: row["id"]
        for row in user_rows
    }

    skill_ids = {
        row["name"]: row["id"]
        for row in skill_rows
    }

    for user in SAMPLE_USERS:
        user_id = user_ids[user["email"]]

        for skill_name in user["skills"]:
            skill_id = skill_ids[skill_name]

            statement = insert(user_skills).values(
                user_id=user_id,
                skill_id=skill_id,
            )

            statement = statement.on_conflict_do_nothing(
                index_elements=[
                    user_skills.c.user_id,
                    user_skills.c.skill_id,
                ],
            )

            connection.execute(statement)


def main():
    """Seed all initial database records."""

    print("Starting database seed...")

    with engine.begin() as connection:
        seed_skills(connection)
        seed_courses(connection)
        seed_users(connection)
        seed_user_skills(connection)

    print("Database seeded successfully.")


if __name__ == "__main__":
    main()