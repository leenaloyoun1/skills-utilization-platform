"""Workflow service."""

from app.workflows.recommendation_workflow import (
    recommendation_workflow,
)


def run_workflow(text):
    """
    Execute the LangGraph workflow.
    """

    return recommendation_workflow.invoke(
        {
            "text": text,
        }
    )