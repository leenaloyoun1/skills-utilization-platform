"""Interactive terminal interface for course recommendations."""

from app.services.database_recommendation_service import (
    recommend_for_user,
)
from app.services.text_recommendation_service import (
    recommend_from_text,
)


def display_recommendations(result):
    """Display recommendations in a readable terminal format."""

    recommendations = result["recommendations"]

    print()
    print("Recommended courses:")
    print("-" * 60)

    for position, course in enumerate(
        recommendations,
        start=1,
    ):
        print()
        print(f"{position}. {course['title']}")
        print(
            f"   Similarity score: "
            f"{course['similarity_score']}"
        )
        print(
            f"   Explanation: "
            f"{course['explanation']}"
        )

    print()
    print(
        "Processing time: "
        f"{result['processing_time_ms']} ms"
    )


def recommend_by_user_id():
    """Ask for a user ID and display recommendations."""

    user_id_text = input(
        "Enter the user ID: "
    ).strip()

    if not user_id_text.isdigit():
        print("The user ID must be a positive integer.")
        return

    user_id = int(user_id_text)

    if user_id <= 0:
        print("The user ID must be greater than zero.")
        return

    try:
        result = recommend_for_user(
            user_id=user_id,
            top_n=3,
        )

        print()
        print(f"User: {result['user']['name']}")
        print(f"Skills: {result['user']['skills']}")

        display_recommendations(result)

    except Exception as error:
        print(f"Recommendation failed: {error}")


def recommend_by_text():
    """Ask for free-form text and display recommendations."""

    text = input(
        "Enter your skills or learning interests: "
    ).strip()

    if not text:
        print("The text cannot be empty.")
        return

    try:
        result = recommend_from_text(
            text=text,
            top_n=3,
        )

        print()
        print("Extracted skills:")
        print(result["skills"])

        display_recommendations(result)

    except Exception as error:
        print(f"Recommendation failed: {error}")


def display_menu():
    """Display the main application menu."""

    print()
    print("=" * 60)
    print("Skills Utilization Platform")
    print("=" * 60)
    print("1. Recommend courses by user ID")
    print("2. Recommend courses from text")
    print("3. Exit")
    print()


def main():
    """Run the interactive terminal application."""

    while True:
        display_menu()

        choice = input(
            "Choose an option: "
        ).strip()

        if choice == "1":
            recommend_by_user_id()

        elif choice == "2":
            recommend_by_text()

        elif choice == "3":
            print("Goodbye!")
            break

        else:
            print(
                "Invalid option. "
                "Please choose 1, 2, or 3."
            )


if __name__ == "__main__":
    main()
