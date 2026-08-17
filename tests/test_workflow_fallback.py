from app.workflows.recommendation_workflow import (
    recommendation_workflow,
)


def main():

    result = recommendation_workflow.invoke(
        {
            "text": (
                "I like pizza and movies"
            )
        }
    )

    print()

    print("Skills:")
    print(result.get("skills"))

    print()

    print("Fallback Used:")
    print(
        result.get(
            "fallback_used",
            False,
        )
    )

    print()

    print("Recommendations:")
    print(
        result.get(
            "recommendations"
        )
    )


if __name__ == "__main__":
    main()