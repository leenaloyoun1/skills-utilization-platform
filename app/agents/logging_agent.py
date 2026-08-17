"""Logging agent."""


def logging_agent(state):
    """
    Record workflow decisions.
    """

    print()
    print("=== WORKFLOW LOG ===")
    print(
        "Skills:",
        state.get("skills"),
    )

    print(
        "Fallback Used:",
        state.get(
            "fallback_used",
            False,
        ),
    )

    recommendation_count = len(
        state.get(
            "recommendations",
            [],
        )
    )

    print(
        "Recommendation Count:",
        recommendation_count,
    )

    return {}