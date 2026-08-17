from app.services.workflow_service import (
    run_workflow,
)


def main():

    result = run_workflow(
        "I want to learn machine learning and NLP"
    )

    print(result)


if __name__ == "__main__":
    main()