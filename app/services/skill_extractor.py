"""Utilities for extracting skills from user-provided text."""

import re


SKILL_ALIASES: dict[str, tuple[str, ...]] = {
    "Artificial Intelligence": (
        "artificial intelligence",
        "ai",
    ),
    "Machine Learning": (
        "machine learning",
        "ml",
    ),
    "Deep Learning": (
        "deep learning",
        "neural networks",
    ),
    "Natural Language Processing": (
        "natural language processing",
        "nlp",
    ),
    "Data Science": (
        "data science",
        "data scientist",
    ),
    "Data Analysis": (
        "data analysis",
        "data analytics",
        "data analyst",
    ),
    "Python": (
        "python",
    ),
    "SQL": (
        "sql",
        "structured query language",
    ),
    "Database Design": (
        "database design",
        "database development",
    ),
    "Backend Development": (
        "backend development",
        "backend",
        "back-end development",
        "back end development",
    ),
    "API Development": (
    "api development",
    "api design",
    "api",
    "apis",
    "rest api",
    "rest apis",
    "restful api",
    "restful apis",
    ),
    "FastAPI": (
        "fastapi",
    ),
    "Git": (
        "git",
        "version control",
    ),
    "GitHub": (
        "github",
    ),
    "Cloud Computing": (
        "cloud computing",
        "cloud development",
    ),
    "Docker": (
        "docker",
        "containerization",
    ),
}


def normalize_text(text: str) -> str:
    """Normalize whitespace and convert text to lowercase."""
    return " ".join(text.lower().strip().split())


def contains_alias(text: str, alias: str) -> bool:
    """Check whether a complete skill alias appears in normalized text."""
    pattern = rf"\b{re.escape(alias)}\b"
    return re.search(pattern, text) is not None


def extract_skills(text: str) -> list[str]:
    """
    Extract standardized skills from user-provided text.

    Args:
        text: A description of the user's skills or learning interests.

    Returns:
        A list containing unique standardized skill names.
    """
    if not isinstance(text, str):
        raise TypeError("Skill-extraction input must be a string.")

    normalized_text = normalize_text(text)

    if not normalized_text:
        return []

    extracted_skills: list[str] = []

    for standard_name, aliases in SKILL_ALIASES.items():
        if any(contains_alias(normalized_text, alias) for alias in aliases):
            extracted_skills.append(standard_name)

    return extracted_skills