"""Display users and their skills from PostgreSQL."""

from app.repositories.user_repository import (
    get_user_with_skills,
)


def display_user(user_id):
    user = get_user_with_skills(user_id)

    print("=" * 60)
    print(f"Requested user ID: {user_id}")

    if user is None:
        print("User not found.")
        return

    print(f"Name: {user['name']}")
    print(f"Email: {user['email']}")
    print(f"Skills: {user['skills']}")


def main():
    display_user(1)
    display_user(2)
    display_user(3)
    display_user(999)


if __name__ == "__main__":
    main()