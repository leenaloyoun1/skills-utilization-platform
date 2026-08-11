from app.services.llm_skill_extractor import (
    extract_skills_with_openai,
)


def main() -> None:
    user_text = (
        "I built predictive systems with Python and worked "
        "on understanding human language."
    )

    print(f"Input: {user_text}")

    skills = extract_skills_with_openai(user_text)

    print(f"Extracted skills: {skills}")


if __name__ == "__main__":
    main()
