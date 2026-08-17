"""Recommendation workflow using LangGraph."""

from typing import TypedDict

from langgraph.graph import END, START, StateGraph

from app.agents.recommendation_agent import (
    recommendation_agent,
)
from app.agents.skill_extraction_agent import (
    skill_extraction_agent,
)

from app.agents.validation_agent import (
    validation_agent,
)

from app.agents.fallback_agent import (
    fallback_agent,
)

from app.agents.logging_agent import (
    logging_agent,
)


class RecommendationState(TypedDict):
    text: str
    skills: list
    valid: bool
    recommendations: list
    fallback_used: bool


def skill_node(state):
    """Run skill extraction."""

    result = skill_extraction_agent(
        state["text"]
    )

    return {
        "skills": result["skills"]
    }


def recommendation_node(state):
    """Run recommendation generation."""

    result = recommendation_agent(
        state["skills"]
    )

    return {
        "recommendations": (
            result["recommendations"]
        )
    }

def validation_node(state):
    """
    Validate extracted skills.
    """

    result = validation_agent(
        state["skills"]
    )

    return {
        "skills": result["skills"],
        "valid": result["valid"],
    }


def fallback_node(state):
    """
    Use default recommendations.
    """

    return fallback_agent()


def validation_router(state):
    """
    Decide workflow path.
    """

    if state["valid"]:
        return "recommend"

    return "fallback"

def logging_node(state):
    return logging_agent(state)



workflow = StateGraph(
    RecommendationState
)

workflow.add_node(
    "skill_extractor",
    skill_node,
)

workflow.add_node(
    "recommender",
    recommendation_node,
)

workflow.add_edge(
    START,
    "skill_extractor",
)

workflow.add_node(
    "validator",
    validation_node,
)

workflow.add_node(
    "fallback",
    fallback_node,
)

workflow.add_edge(
    "skill_extractor",
    "validator",
)

workflow.add_conditional_edges(
    "validator",
    validation_router,
    {
        "recommend": "recommender",
        "fallback": "fallback",
    },
)

workflow.add_node(
    "logger",
    logging_node,
)

workflow.add_edge(
    "fallback",
    "logger",
)

workflow.add_edge(
    "fallback",
    END,
)

workflow.add_edge(
    "recommender",
    "logger",
)

workflow.add_edge(
    "logger",
    END,
)



recommendation_workflow = (
    workflow.compile()
)