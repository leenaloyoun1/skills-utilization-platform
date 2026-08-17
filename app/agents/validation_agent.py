"""Validation agent."""

ALLOWED_SKILLS = {
    "Artificial Intelligence",
    "Machine Learning",
    "Deep Learning",
    "Natural Language Processing",
    "Data Science",
    "Data Analysis",
    "Python",
    "SQL",
    "Database Design",
    "Backend Development",
    "API Development",
    "FastAPI",
    "Git",
    "GitHub",
    "Cloud Computing",
    "Docker",
}


def validation_agent(skills):
    """
    Validate extracted skills.
    """

    valid_skills = [
        skill
        for skill in skills
        if skill in ALLOWED_SKILLS
    ]

    return {
        "skills": valid_skills,
        "valid": len(valid_skills) > 0,
    }