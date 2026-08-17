"""Recommendation agent."""

from app.services.stored_recommendation_service import (
    recommend_from_stored_skills,
)


def recommendation_agent(skills, top_n=3):
    """
    Generate recommendations from skills.
    """

    recommendations = recommend_from_stored_skills(
        skills=skills,
        top_n=top_n,
    )

    return {
        "skills": skills,
        "recommendations": recommendations,
    }