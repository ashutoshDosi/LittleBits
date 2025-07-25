"""
executor.py
Handles communication with Google Gemini API.
"""

import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file.")

genai.configure(api_key=GEMINI_API_KEY)

def call_gemini(prompt: str) -> str:
    """
    Sends a prompt to the Gemini API and returns the response text.
    Args:
        prompt (str): The prompt to send to Gemini.
    Returns:
        str: The response from Gemini.
    """
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt)
    return response.text if hasattr(response, 'text') else str(response) 