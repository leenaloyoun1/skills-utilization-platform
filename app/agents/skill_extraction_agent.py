"""Skill extraction agent."""

from app.services.llm_skill_extractor import (
    extract_skills_with_openai,
)


def skill_extraction_agent(text):
    """
    Extract skills from user text.
    """

    skills = extract_skills_with_openai(text)

    return {
        "text": text,
        "skills": skills,
    }