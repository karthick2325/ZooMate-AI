
import time

from google import genai
from google.genai import errors

from config import GEMINI_API_KEY


# Gemini model configuration
MODEL_NAME = "gemini-3.5-flash-lite"
MAX_RETRIES = 3

# Initialize Gemini client
client = genai.Client(
    api_key=GEMINI_API_KEY,
    http_options={
        "timeout": 60000
    }
)


def get_gemini_response(prompt: str) -> str:
    """
    Generate a response using Gemini API.
    Handles temporary server errors and API failures.
    """

    if not prompt or not prompt.strip():
        return "Please enter a valid question."

    for attempt in range(MAX_RETRIES):

        try:
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt
            )

            if response and response.text:
                return response.text.strip()

            return "Gemini returned an empty response. Please try again."

        except errors.APIError as e:

            error_code = getattr(e, "code", None)

            # Retry temporary server errors
            if error_code in (429, 500, 502, 503, 504):

                if attempt < MAX_RETRIES - 1:
                    wait_time = 2 ** (attempt + 1)

                    print(
                        f"Gemini temporarily unavailable. "
                        f"Retrying in {wait_time} seconds..."
                    )

                    time.sleep(wait_time)
                    continue

                return (
                    "Gemini is currently busy. "
                    "Please try again after some time."
                )

            # Other API errors
            return f"Gemini API Error ({error_code}): {e}"

        except Exception as e:

            return f"Unexpected Error: {e}"

    return "Unable to generate a response. Please try again."
