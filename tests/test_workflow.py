from app.workflows.recommendation_workflow import (
    recommendation_workflow,
)


def main():

    result = recommendation_workflow.invoke(
        {
            "text": (
                "I want to learn machine learning "
                "and natural language processing"
            )
        }
    )

    print()

    print("Skills:")
    print(result["skills"])

    print()

    print("Recommendations:")

    for recommendation in result[
        "recommendations"
    ]:

        print(
            recommendation["title"]
        )


if __name__ == "__main__":
    main()