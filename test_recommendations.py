import json
from pathlib import Path

from app.services.llm_skill_extractor import (
    extract_skills_with_openai,
)
from app.services.recommendation_service import recommend_courses


COURSES_FILE = Path("data/courses.json")


def load_courses():
    with COURSES_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def display_recommendations(user_text, top_n=3):
    print("=" * 70)
    print(f"User input: {user_text}")

    skills = extract_skills_with_openai(user_text)

    print(f"Extracted skills: {skills}")

    if not skills:
        print("No recognized skills were found.")
        return

    courses = load_courses()

    recommendations = recommend_courses(
        skills=skills,
        courses=courses,
        top_n=top_n,
    )

    print()
    print(f"Top {len(recommendations)} recommendations:")

    for position, recommendation in enumerate(
        recommendations,
        start=1,
    ):
        print()
        print(f"{position}. {recommendation['title']}")
        print(
            f"   Similarity score: "
            f"{recommendation['similarity_score']}"
        )
        print(
            f"   Explanation: "
            f"{recommendation['explanation']}"
        )


def main():
    user_texts = [
        (
            "I want to learn Python, build backend applications, "
            "and create REST APIs."
        ),
        (
            "I am interested in artificial intelligence, "
            "machine learning, and understanding human language."
        ),
        (
            "I want to learn SQL queries, relational databases, "
            "table relationships, and database design."
        ),
    ]

    for user_text in user_texts:
        display_recommendations(
            user_text=user_text,
            top_n=3,
        )

        print()

if __name__ == "__main__":
    main()