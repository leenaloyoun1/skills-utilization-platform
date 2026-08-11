from app.repositories.course_repository import (
    get_all_courses,
    get_course_embeddings,
)


def main():
    courses = get_all_courses()

    print("Courses:")
    print(f"Count: {len(courses)}")

    print()
    print(courses[0]["title"])

    embeddings = get_course_embeddings()

    print()
    print("Course embeddings:")
    print(f"Count: {len(embeddings)}")

    print()
    print(
        "Dimensions:",
        len(embeddings[0]["vector"]),
    )


if __name__ == "__main__":
    main()