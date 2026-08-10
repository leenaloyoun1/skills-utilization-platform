"""Recommend courses using semantic similarity."""

from typing import Any

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from app.services.embedding_service import generate_course_embeddings
from app.services.profile_service import build_user_profile


def build_course_text(course: dict[str, Any]) -> str:
    """Combine course information into text for embedding generation."""

    title = course.get("title", "")
    description = course.get("description", "")
    skills = course.get("skills", [])

    skills_text = ", ".join(skills)

    return (
        f"Course title: {title}. "
        f"Description: {description} "
        f"Skills taught: {skills_text}."
    )


def calculate_similarity_scores(
    user_profile: np.ndarray,
    course_embeddings: np.ndarray,
) -> np.ndarray:
    """Calculate cosine similarity between a user and all courses."""

    if user_profile.ndim != 1:
        raise ValueError(
            "The user-profile vector must be one-dimensional."
        )

    if course_embeddings.ndim != 2:
        raise ValueError(
            "Course embeddings must be two-dimensional."
        )

    if user_profile.shape[0] != course_embeddings.shape[1]:
        raise ValueError(
            "User and course embeddings must have matching dimensions."
        )

    user_profile_2d = user_profile.reshape(1, -1)

    scores = cosine_similarity(
        user_profile_2d,
        course_embeddings,
    )[0]

    return scores


def create_explanation(
    user_skills: list[str],
    course: dict[str, Any],
) -> str:
    """Create a simple explanation for a course recommendation."""

    course_skills = course.get("skills", [])

    matching_skills = [
        skill
        for skill in user_skills
        if skill in course_skills
    ]

    if matching_skills:
        matched_text = ", ".join(matching_skills)

        return (
            f"This course directly matches these user skills: "
            f"{matched_text}."
        )

    user_skills_text = ", ".join(user_skills)

    return (
        f"This course is semantically related to the user's "
        f"interests in {user_skills_text}."
    )


def recommend_courses(
    skills: list[str],
    courses: list[dict[str, Any]],
    top_n: int = 3,
) -> list[dict[str, Any]]:
    """
    Rank courses according to semantic similarity.

    Args:
        skills: Standardized user skills.
        courses: Available course dictionaries.
        top_n: Maximum number of recommendations.

    Returns:
        Ranked course recommendations with scores and explanations.
    """

    if not skills:
        raise ValueError(
            "At least one skill is required for recommendations."
        )

    if not courses:
        raise ValueError(
            "At least one course is required for recommendations."
        )

    if top_n <= 0:
        raise ValueError(
            "top_n must be greater than zero."
        )

    user_profile = build_user_profile(skills)

    course_texts = [
        build_course_text(course)
        for course in courses
    ]

    course_embeddings = generate_course_embeddings(course_texts)

    similarity_scores = calculate_similarity_scores(
        user_profile,
        course_embeddings,
    )

    ranked_indices = np.argsort(similarity_scores)[::-1]

    recommendation_count = min(top_n, len(courses))

    recommendations: list[dict[str, Any]] = []

    for index in ranked_indices[:recommendation_count]:
        course = courses[int(index)]
        score = float(similarity_scores[int(index)])

        recommendations.append(
            {
                "course_id": course["id"],
                "title": course["title"],
                "similarity_score": round(score, 4),
                "explanation": create_explanation(
                    skills,
                    course,
                ),
            }
        )

    return recommendations