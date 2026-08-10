"""Build a user-profile vector from multiple skill embeddings."""

import numpy as np

from app.services.embedding_service import generate_skill_embeddings


def average_embeddings(embeddings: np.ndarray) -> np.ndarray:
    """Combine multiple skill embeddings using average pooling."""

    if embeddings.ndim != 2:
        raise ValueError(
            "Embeddings must be a two-dimensional array."
        )

    if embeddings.shape[0] == 0:
        raise ValueError(
            "At least one skill embedding is required."
        )

    profile_vector = np.mean(
        embeddings,
        axis=0,
        dtype=np.float32,
    )

    vector_length = np.linalg.norm(profile_vector)

    if vector_length == 0:
        raise ValueError(
            "The user-profile vector cannot have zero length."
        )

    normalized_profile = profile_vector / vector_length

    return np.asarray(normalized_profile, dtype=np.float32)


def build_user_profile(skills: list[str]) -> np.ndarray:
    """Generate skill embeddings and combine them into one profile."""

    if not skills:
        raise ValueError(
            "At least one skill is required to build a profile."
        )

    skill_embeddings = generate_skill_embeddings(skills)

    return average_embeddings(skill_embeddings)