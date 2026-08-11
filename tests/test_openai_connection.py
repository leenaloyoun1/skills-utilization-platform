"""Test the OpenAI API connection without displaying the API key."""

import os

from dotenv import load_dotenv
from openai import OpenAI


def main() -> None:
    load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY")
    model_name = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    if not api_key:
        print("OPENAI_API_KEY was not found in .env.")
        return

    print("API key was loaded securely from .env.")
    print(f"Testing model: {model_name}")

    client = OpenAI(api_key=api_key)

    try:
        response = client.responses.create(
            model=model_name,
            instructions=(
                "Respond using only the single word: connected"
            ),
            input="Test the API connection.",
        )

        print(f"OpenAI response: {response.output_text}")

    except Exception as error:
        print("The OpenAI request failed.")
        print(f"Error type: {type(error).__name__}")
        print(f"Error message: {error}")


if __name__ == "__main__":
    main()