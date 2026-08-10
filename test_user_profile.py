"""Manually test user-profile vector generation."""

import numpy as np

from app.services.profile_service import build_user_profile


def main() -> None:
    skills = [
        "Python",
        "Machine Learning",
        "Backend Development",
    ]

    print("User skills:")
    print(skills)

    print()
    print("Building user-profile vector...")

    user_profile = build_user_profile(skills)

    print()
    print("User-profile shape:")
    print(user_profile.shape)

    print()
    print("First five profile values:")
    print(user_profile[:5])

    print()
    print("Profile vector length:")
    print(np.linalg.norm(user_profile))

    print()
    print("User-profile vector generated successfully.")


if __name__ == "__main__":
    main()