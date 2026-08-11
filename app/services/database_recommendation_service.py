"""Generate recommendations using stored PostgreSQL embeddings."""

import time

import numpy as np

from app.repositories.embedding_repository import (
    get_courses_with_embeddings,
    get_skill_embeddings,
)
from app.repositories.recommendation_repository import (
    log_recommendation,
)
from app.repositories.user_repository import (
    get_user_with_skills,
)
from app.services.profile_service import average_embeddings
from app.services.recommendation_service import (
    calculate_similarity_scores,
    create_explanation,
)


def recommend_for_user(user_id, top_n=3):
    """Generate recommendations for a database user."""

    start_time = time.perf_counter()

    if top_n <= 0:
        raise ValueError(
            "top_n must be greater than zero."
        )

    user = get_user_with_skills(user_id)

    if user is None:
        raise ValueError(
            f"User {user_id} was not found."
        )

    if not user["skills"]:
        raise ValueError(
            f"User {user_id} has no stored skills."
        )

    skill_records = get_skill_embeddings(
        user["skills"]
    )

    if len(skill_records) != len(user["skills"]):
        found_skills = {
            record["skill_name"]
            for record in skill_records
        }

        missing_skills = [
            skill
            for skill in user["skills"]
            if skill not in found_skills
        ]

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
            "No courses with embeddings were found."
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

        recommendations.append(
            {
                "course_id": course["course_id"],
                "title": course["title"],
                "similarity_score": round(score, 4),
                "explanation": create_explanation(
                    user["skills"],
                    course_data,
                ),
            }
        )

    processing_time_ms = (
        time.perf_counter() - start_time
    ) * 1000

    log_recommendation(
        user_id=user_id,
        input_text=None,
        extracted_skills=user["skills"],
        recommended_courses=recommendations,
        top_n=top_n,
        status="success",
        processing_time_ms=round(
            processing_time_ms,
            2,
        ),
    )

    return {
        "user": user,
        "recommendations": recommendations,
        "processing_time_ms": round(
            processing_time_ms,
            2,
        ),
    }