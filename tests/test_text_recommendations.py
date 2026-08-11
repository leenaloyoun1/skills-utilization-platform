from app.services.text_recommendation_service import (
    recommend_from_text,
)


def main():

    text = (
        "I want to learn artificial intelligence, "
        "machine learning and natural language processing."
    )

    result = recommend_from_text(text)

    print()
    print("Extracted skills:")
    print(result["skills"])

    print()
    print("Recommendations:")

    for course in result["recommendations"]:
        print()
        print(course["title"])
        print(course["similarity_score"])


if __name__ == "__main__":
    main()