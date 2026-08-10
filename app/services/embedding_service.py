"""Generate vector embeddings for skills and course descriptions."""

from collections.abc import Sequence

import numpy as np
from numpy.typing import NDArray
from sentence_transformers import SentenceTransformer


DEFAULT_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

_model: SentenceTransformer | None = None


def get_embedding_model(
    model_name: str = DEFAULT_MODEL_NAME,
) -> SentenceTransformer:
    """
    Load and cache the Sentence Transformer model.

    The first call loads the model. Later calls reuse the same model
    instead of loading it again.
    """
    global _model

    if _model is None:
        print(f"Loading embedding model: {model_name}")
        _model = SentenceTransformer(model_name)

    return _model


def validate_texts(texts: Sequence[str]) -> list:
    """Validate and clean a sequence of text values."""
    if isinstance(texts, str):
        raise TypeError(
            "Expected a sequence of strings, not one string."
        )

    cleaned_texts: list[str] = []

    for text in texts:
        if not isinstance(text, str):
            raise TypeError(
                "Every embedding input must be a string."
            )

        cleaned_text = " ".join(text.strip().split())

        if cleaned_text:
            cleaned_texts.append(cleaned_text)

    if not cleaned_texts:
        raise ValueError(
            "At least one non-empty text value is required."
        )

    return cleaned_texts


def generate_embeddings(
    texts: Sequence[str],
) -> NDArray[np.float32]:
    """
    Convert multiple text values into normalized embedding vectors.

    Args:
        texts: Skills, course descriptions, or other text values.

    Returns:
        A two-dimensional NumPy array. Each row is one embedding.
    """
    cleaned_texts = validate_texts(texts)
    model = get_embedding_model()

    embeddings = model.encode(
        cleaned_texts,
        convert_to_numpy=True,
        normalize_embeddings=True,
        show_progress_bar=False,
    )

    return np.asarray(embeddings, dtype=np.float32)


def generate_skill_embeddings(
    skills: Sequence[str],
) -> NDArray[np.float32]:
    """Generate one embedding vector for each skill."""
    return generate_embeddings(skills)


def generate_course_embeddings(
    course_descriptions: Sequence[str],
) -> NDArray[np.float32]:
    """Generate one embedding vector for each course description."""
    return generate_embeddings(course_descriptions)