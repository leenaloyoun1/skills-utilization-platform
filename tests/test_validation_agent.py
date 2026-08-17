from app.agents.validation_agent import (
    validation_agent,
)


def main():

    result = validation_agent(
        [
            "Machine Learning",
            "Unknown Skill",
            "Natural Language Processing",
        ]
    )

    print(result)


if __name__ == "__main__":
    main()