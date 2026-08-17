"""Fallback agent."""


def fallback_agent():
    """
    Return default recommendations.
    """

    return {
        "recommendations": [
            {
                "title": (
                    "Python Programming Fundamentals"
                ),
                "similarity_score": 0.0,
                "explanation": (
                    "Default recommendation because "
                    "no valid skills were identified."
                ),
            },
            {
                "title": (
                    "Data Analysis with Python"
                ),
                "similarity_score": 0.0,
                "explanation": (
                    "Default recommendation because "
                    "no valid skills were identified."
                ),
            },
            {
                "title": (
                    "SQL and Database Design"
                ),
                "similarity_score": 0.0,
                "explanation": (
                    "Default recommendation because "
                    "no valid skills were identified."
                ),
            },
        ],
        "fallback_used": True,
    }