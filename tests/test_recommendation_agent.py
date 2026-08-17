from app.agents.recommendation_agent import (
    recommendation_agent,
)


def main():

    result = recommendation_agent(
        [
            "Machine Learning",
            "Natural Language Processing",
        ]
    )

    print()

    print("Skills:")
    print(result["skills"])

    print()

    print("Recommendations:")

    for recommendation in result["recommendations"]:

        print(
            recommendation["title"]
        )


if __name__ == "__main__":
    main()