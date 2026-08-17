from app.agents.skill_extraction_agent import (
    skill_extraction_agent,
)


def main():

    result = skill_extraction_agent(
        "I want to learn machine learning and NLP"
    )

    print(result)


if __name__ == "__main__":
    main()