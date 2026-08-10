"""Manually test skill and course embedding generation."""

import json
from pathlib import Path

from app.services.embedding_service import (
    generate_course_embeddings,
    generate_skill_embeddings,
)


COURSES_FILE = Path("data/courses.json")


def load_courses() -> list: 
    """Read sample courses from the JSON data file."""
    with COURSES_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def main() -> None:
    skills = [
        "Python",
        "Machine Learning",
        "Backend Development",
    ]

    courses = load_courses()
    course_descriptions = [
        course["description"]
        for course in courses
    ]

    print("Generating skill embeddings...")
    skill_embeddings = generate_skill_embeddings(skills)

    print("Generating course embeddings...")
    course_embeddings = generate_course_embeddings(
        course_descriptions
    )

    print()
    print("Skills:")
    print(skills)

    print()
    print("Skill embedding shape:")
    print(skill_embeddings.shape)

    print()
    print("Number of courses:")
    print(len(courses))

    print()
    print("Course embedding shape:")
    print(course_embeddings.shape)

    print()
    print("First five values of the Python embedding:")
    print(skill_embeddings[0][:5])

    print()
    print("Embedding generation completed successfully.")


if __name__ == "__main__":
    main()
    