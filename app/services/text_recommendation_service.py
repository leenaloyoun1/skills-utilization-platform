"""Generate database-backed recommendations from user text."""

import time

from app.repositories.recommendation_repository import (
    log_recommendation,
)
from app.services.llm_skill_extractor import (
    extract_skills_with_openai,
)
from app.services.stored_recommendation_service import (
    recommend_from_stored_skills,
)


def recommend_from_text(text, top_n=3):
    """Generate recommendations from free-form user text."""

    start_time = time.perf_counter()

    if not isinstance(text, str):
        raise TypeError(
            "Recommendation input must be a string."
        )

    cleaned_text = " ".join(
        text.strip().split()
    )

    if not cleaned_text:
        raise ValueError(
            "Recommendation text cannot be empty."
        )

    if top_n <= 0:
        raise ValueError(
            "top_n must be greater than zero."
        )

    skills = extract_skills_with_openai(
        cleaned_text
    )

    if not skills:
        raise ValueError(
            "No recognized skills were identified."
        )

    recommendations = recommend_from_stored_skills(
        skills=skills,
        top_n=top_n,
    )

    processing_time_ms = (
        time.perf_counter() - start_time
    ) * 1000

    log_recommendation(
        user_id=None,
        input_text=cleaned_text,
        extracted_skills=skills,
        recommended_courses=recommendations,
        top_n=top_n,
        status="success",
        processing_time_ms=round(
            processing_time_ms,
            2,
        ),
    )

    return {
        "text": cleaned_text,
        "skills": skills,
        "recommendations": recommendations,
        "processing_time_ms": round(
            processing_time_ms,
            2,
        ),
    }