import json
import os
import traceback
from dotenv import load_dotenv
from openai import OpenAI

from app.services.skill_extractor import extract_skills


load_dotenv()


ALLOWED_SKILLS = [
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
]


def clean_llm_skills(skills):
    if not isinstance(skills, list):
        return []

    cleaned_skills = []

    for skill in skills:
        if (
            isinstance(skill, str)
            and skill in ALLOWED_SKILLS
            and skill not in cleaned_skills
        ):
            cleaned_skills.append(skill)

    return cleaned_skills


def extract_skills_with_openai(text: str) -> list[str]:
    if not isinstance(text, str):
        raise TypeError(
            "Skill-extraction input must be a string."
        )

    cleaned_text = " ".join(text.strip().split())

    if not cleaned_text:
        return []

    api_key = os.getenv("OPENAI_API_KEY")
    model_name = os.getenv(
        "OPENAI_MODEL",
        "gpt-4o-mini",
    )

    if not api_key:
        print(
            "OpenAI key is unavailable. "
            "Using the predefined extractor."
        )
        return extract_skills(cleaned_text)

    client = OpenAI(api_key=api_key)

    allowed_skills_text = ", ".join(ALLOWED_SKILLS)

    instructions = (
        "Extract technical skills from user-provided text. "
        "Return only a valid JSON array of strings. "
        "Do not return Markdown, code fences, or explanations. "
        "Use only skills from this allowed list: "
        f"{allowed_skills_text}. "
        "Return an empty JSON array when no allowed skill is relevant."
    )

    try:
        response = client.responses.create(
            model=model_name,
            instructions=instructions,
            input=cleaned_text,
        )


        response_text = response.output_text.strip()
        parsed_result = json.loads(response_text)
        llm_skills = clean_llm_skills(parsed_result)

        if llm_skills:
            return llm_skills

        return extract_skills(cleaned_text)

    except Exception as error:
        traceback.print_exc()

        print(
            "OpenAI extraction failed. "
            "Using the predefined extractor."
        )
        print(f"Reason: {type(error).__name__}")
        print(f"Details: {error}")
        

        return extract_skills(cleaned_text)