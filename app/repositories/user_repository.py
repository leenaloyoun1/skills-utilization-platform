"""Database queries related to users and their skills."""

from sqlalchemy import select

from app.db.engine import engine
from app.db.tables import skills, user_skills, users


def get_user_by_id(user_id):
    """Retrieve one user by ID."""

    statement = (
        select(
            users.c.id,
            users.c.name,
            users.c.email,
            users.c.created_at,
        )
        .where(users.c.id == user_id)
    )

    with engine.connect() as connection:
        user = connection.execute(
            statement
        ).mappings().first()

    if user is None:
        return None

    return dict(user)


def get_user_skills(user_id):
    """Retrieve the standardized skills belonging to a user."""

    statement = (
        select(skills.c.name)
        .select_from(
            user_skills.join(
                skills,
                user_skills.c.skill_id == skills.c.id,
            )
        )
        .where(user_skills.c.user_id == user_id)
        .order_by(skills.c.name)
    )

    with engine.connect() as connection:
        rows = connection.execute(statement).all()

    skill_names = []

    for row in rows:
        skill_names.append(row.name)

    return skill_names


def get_user_with_skills(user_id):
    """Retrieve one user together with the user's skills."""

    user = get_user_by_id(user_id)

    if user is None:
        return None

    user["skills"] = get_user_skills(user_id)

    return user