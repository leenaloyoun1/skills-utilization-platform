from app.services.database_recommendation_service import (
    recommend_for_user,
)


def display_recommendations(user_id):
    print("=" * 60)

    try:
        result = recommend_for_user(user_id)

        print(
            f"User: {result['user']['name']}"
        )

        print(
            f"Skills: {result['user']['skills']}"
        )

        print()
        print("Recommendations:")

        for course in result["recommendations"]:
            print()
            print(
                f"- {course['title']}"
            )
            print(
                f"  Score: "
                f"{course['similarity_score']}"
            )

    except Exception as error:
        print(error)


def main():
    display_recommendations(1)
    display_recommendations(2)
    display_recommendations(3)
    display_recommendations(999)


if __name__ == "__main__":
    main()