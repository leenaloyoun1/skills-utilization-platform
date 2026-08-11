"""Test recommendations using stored PostgreSQL embeddings."""

from app.services.stored_recommendation_service import (
    recommend_from_stored_skills,
)


def main():
    skills = [
        "Python",
        "Backend Development",
        "API Development",
    ]

    print("Skills:")
    print(skills)

    recommendations = recommend_from_stored_skills(
        skills=skills,
        top_n=3,
    )

    print()
    print("Recommendations:")

    for recommendation in recommendations:
        print()
        print(recommendation["title"])
        print(
            "Score:",
            recommendation["similarity_score"],
        )
        print(
            "Explanation:",
            recommendation["explanation"],
        )


if __name__ == "__main__":
    main()