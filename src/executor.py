"""
executor.py
Handles communication with Google Gemini API for CycleWise.

- Loads Gemini API key from .env
- Exports call_gemini(prompt: str) -> str
- Adds robust error handling and logging
- Handles flexible Gemini response formats
"""

import os
import logging
from dotenv import load_dotenv
import google.generativeai as genai
from typing import Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file.")

genai.configure(api_key=GEMINI_API_KEY)

def call_gemini(prompt: str) -> str:
    """
    Sends a prompt to the Gemini API and returns the response text.
    Logs the prompt and response. Handles errors and flexible response formats.

    Args:
        prompt (str): The prompt to send to Gemini.
    Returns:
        str: The response from Gemini.
    Raises:
        RuntimeError: If the API call fails or response is invalid.
    """
    logger.info(f"Sending prompt to Gemini: {prompt}")
    try:
        model = genai.GenerativeModel("gemini-pro")
        response: Any = model.generate_content(prompt)
        logger.info(f"Raw Gemini response: {response}")

        # Check for response text
        if hasattr(response, "text") and response.text:
            logger.info(f"Gemini response text: {response.text}")
            return response.text

        # Fallback: check for candidates
        if isinstance(response, dict) and "candidates" in response:
            candidates = response["candidates"]
            if candidates and "content" in candidates[0] and "parts" in candidates[0]["content"]:
                parts = candidates[0]["content"]["parts"]
                if parts and isinstance(parts[0], str):
                    logger.info(f"Gemini response (candidates): {parts[0]}")
                    return parts[0]

        logger.warning("Unexpected Gemini response format; returning stringified version.")
        return str(response)

    except Exception as e:
        logger.error(f"Error communicating with Gemini API: {e}")
        raise RuntimeError(f"Gemini API call failed: {e}")
