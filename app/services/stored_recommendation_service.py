"""Rank courses using embeddings stored in PostgreSQL."""

import numpy as np

from app.repositories.embedding_repository import (
    get_courses_with_embeddings,
    get_skill_embeddings,
)
from app.services.profile_service import average_embeddings
from app.services.recommendation_service import (
    calculate_similarity_scores,
    create_explanation,
)


def recommend_from_stored_skills(skills, top_n=3):
    """Recommend courses using stored skill and course vectors."""

    if not skills:
        raise ValueError(
            "At least one skill is required."
        )

    if top_n <= 0:
        raise ValueError(
            "top_n must be greater than zero."
        )

    skill_records = get_skill_embeddings(skills)

    found_skills = {
        record["skill_name"]
        for record in skill_records
    }

    missing_skills = [
        skill
        for skill in skills
        if skill not in found_skills
    ]

    if missing_skills:
        raise ValueError(
            "Stored embeddings were not found for: "
            + ", ".join(missing_skills)
        )

    skill_vectors = np.asarray(
        [
            record["vector"]
            for record in skill_records
        ],
        dtype=np.float32,
    )

    user_profile = average_embeddings(
        skill_vectors
    )

    course_records = get_courses_with_embeddings()

    if not course_records:
        raise ValueError(
            "No courses with stored embeddings were found."
        )

    course_vectors = np.asarray(
        [
            record["vector"]
            for record in course_records
        ],
        dtype=np.float32,
    )

    similarity_scores = calculate_similarity_scores(
        user_profile,
        course_vectors,
    )

    ranked_indices = np.argsort(
        similarity_scores
    )[::-1]

    recommendation_count = min(
        top_n,
        len(course_records),
    )

    recommendations = []

    for index in ranked_indices[:recommendation_count]:
        course = course_records[int(index)]
        score = float(
            similarity_scores[int(index)]
        )

        course_data = {
            "id": course["course_id"],
            "title": course["title"],
            "description": course["description"],
            "skills": course["skills"],
        }

        recommendation = {
            "course_id": course["course_id"],
            "title": course["title"],
            "similarity_score": round(score, 4),
            "explanation": create_explanation(
                skills,
                course_data,
            ),
        }

        recommendations.append(recommendation)

    return recommendations