"""Test retrieval of stored embeddings from PostgreSQL."""

from app.repositories.embedding_repository import (
    get_courses_with_embeddings,
    get_skill_embeddings,
)


def main():
    requested_skills = [
        "Python",
        "SQL",
        "Backend Development",
    ]

    skill_records = get_skill_embeddings(
        requested_skills
    )

    print("=" * 60)
    print("Requested skills:")
    print(requested_skills)

    print()
    print("Stored skill embeddings found:")
    print(len(skill_records))

    for record in skill_records:
        print(
            f"- {record['skill_name']}: "
            f"{record['dimensions']} dimensions"
        )

    course_records = get_courses_with_embeddings()

    print()
    print("=" * 60)
    print("Courses with stored embeddings:")
    print(len(course_records))

    if course_records:
        first_course = course_records[0]

        print()
        print("First course:")
        print(first_course["title"])

        print(
            "Stored dimensions:",
            first_course["dimensions"],
        )

        print(
            "Actual vector length:",
            len(first_course["vector"]),
        )


if __name__ == "__main__":
    main()