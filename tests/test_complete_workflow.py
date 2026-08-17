from app.workflows.recommendation_workflow import (
    recommendation_workflow,
)


def test_input(text):

    print()
    print("=" * 60)

    print("Input:")
    print(text)

    result = recommendation_workflow.invoke(
        {
            "text": text
        }
    )

    print()
    print("Skills:")
    print(result.get("skills"))

    print()
    print(
        "Fallback Used:",
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


def main():

    test_input(
        "I want to learn machine learning and NLP"
    )

    test_input(
        "I want to learn backend development"
    )

    test_input(
        "I like pizza and movies"
    )


if __name__ == "__main__":
    main()