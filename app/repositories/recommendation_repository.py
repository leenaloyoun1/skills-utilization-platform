"""Database queries related to recommendation logging."""

from sqlalchemy.dialects.postgresql import insert

from app.db.engine import engine
from app.db.tables import recommendation_logs


def log_recommendation(
    user_id,
    input_text,
    extracted_skills,
    recommended_courses,
    top_n,
    status="success",
    error_message=None,
    processing_time_ms=None,
):
    """Save one recommendation request."""

    statement = insert(
        recommendation_logs
    ).values(
        user_id=user_id,
        input_text=input_text,
        extracted_skills=extracted_skills,
        recommended_courses=recommended_courses,
        top_n=top_n,
        status=status,
        error_message=error_message,
        processing_time_ms=processing_time_ms,
    )

    with engine.begin() as connection:
        connection.execute(statement)