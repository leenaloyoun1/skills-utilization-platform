"""Flask API for the Skills Utilization Platform."""

from flask import Flask, jsonify, request, render_template

from app.core.config import settings
from app.services.database_recommendation_service import (
    recommend_for_user,
)
from app.services.text_recommendation_service import (
    recommend_from_text,
)
from app.services.workflow_service import (
    run_workflow,
)


app = Flask(__name__)


@app.get("/")
def home():
    """Display the visual recommendation interface."""

    return render_template("index.html")


@app.get("/api/health")
def health_check():
    """Return a simple API health response."""

    return jsonify(
        {
            "status": "healthy",
        }
    )

@app.post("/recommend")
def recommend_web():
    """Process recommendations submitted through the webpage."""

    input_type = request.form.get(
        "input_type",
        "text",
    )

    top_n_text = request.form.get(
        "top_n",
        "3",
    )

    try:
        top_n = int(top_n_text)

        if top_n <= 0:
            raise ValueError(
                "Top N must be greater than zero."
            )

        if input_type == "user_id":
            user_id_text = request.form.get(
                "user_id",
                "",
            ).strip()

            if not user_id_text.isdigit():
                raise ValueError(
                    "User ID must be a positive integer."
                )

            result = recommend_for_user(
                user_id=int(user_id_text),
                top_n=top_n,
            )

            return render_template(
                "index.html",
                input_type="user_id",
                user_id=user_id_text,
                top_n=top_n,
                user=result["user"],
                extracted_skills=(
                    result["user"]["skills"]
                ),
                recommendations=(
                    result["recommendations"]
                ),
                processing_time_ms=(
                    result["processing_time_ms"]
                ),
            )

        text = request.form.get(
            "text",
            "",
        ).strip()

        if not text:
            raise ValueError(
                "Please enter your skills or learning interests."
            )

        result = run_workflow(text)

        return render_template(
            "index.html",
            input_type="text",
            text=text,
            top_n=top_n,
            extracted_skills=result["skills"],
            recommendations=result["recommendations"],
            processing_time_ms="Workflow",
        )

    except Exception as error:
        return render_template(
            "index.html",
            input_type=input_type,
            user_id=request.form.get(
                "user_id",
                "",
            ),
            text=request.form.get(
                "text",
                "",
            ),
            top_n=top_n_text,
            error_message=str(error),
        )


@app.post("/api/recommend")
def recommend():
    """Generate recommendations from a user ID or text."""

    request_data = request.get_json(
        silent=True
    )

    if request_data is None:
        return jsonify(
            {
                "error": (
                    "The request body must contain valid JSON."
                )
            }
        ), 400

    user_id = request_data.get("user_id")
    text = request_data.get("text")
    top_n = request_data.get(
        "top_n",
        settings.default_top_n,
    )

    if user_id is not None and text is not None:
        return jsonify(
            {
                "error": (
                    "Provide either user_id or text, "
                    "not both."
                )
            }
        ), 400

    if user_id is None and text is None:
        return jsonify(
            {
                "error": (
                    "Provide either user_id or text."
                )
            }
        ), 400

    if (
        not isinstance(top_n, int)
        or isinstance(top_n, bool)
        or top_n <= 0
    ):
        return jsonify(
            {
                "error": (
                    "top_n must be a positive integer."
                )
            }
        ), 400

    try:
        if user_id is not None:
            if (
                not isinstance(user_id, int)
                or isinstance(user_id, bool)
                or user_id <= 0
            ):
                return jsonify(
                    {
                        "error": (
                            "user_id must be a "
                            "positive integer."
                        )
                    }
                ), 400

            result = recommend_for_user(
                user_id=user_id,
                top_n=top_n,
            )

            return jsonify(
                {
                    "input_type": "user_id",
                    "user_id": result["user"]["id"],
                    "user_name": result["user"]["name"],
                    "extracted_skills": (
                        result["user"]["skills"]
                    ),
                    "recommended_courses": (
                        result["recommendations"]
                    ),
                    "processing_time_ms": (
                        result["processing_time_ms"]
                    ),
                }
            ), 200

        if not isinstance(text, str):
            return jsonify(
                {
                    "error": "text must be a string."
                }
            ), 400

        result = recommend_from_text(
            text=text,
            top_n=top_n,
        )

        return jsonify(
            {
                "input_type": "text",
                "input_text": result["text"],
                "extracted_skills": result["skills"],
                "recommended_courses": (
                    result["recommendations"]
                ),
                "processing_time_ms": (
                    result["processing_time_ms"]
                ),
            }
        ), 200

    except ValueError as error:
        return jsonify(
            {
                "error": str(error),
            }
        ), 404

    except Exception as error:
        print(
            f"Unexpected recommendation error: "
            f"{type(error).__name__}: {error}"
        )

        return jsonify(
            {
                "error": (
                    "An unexpected error occurred "
                    "while generating recommendations."
                )
            }
        ), 500