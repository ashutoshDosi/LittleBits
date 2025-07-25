"""
memory.py
Logs user interactions to a local JSON file.
"""

import json
from datetime import datetime
from pathlib import Path

LOG_FILE = Path(__file__).parent / "interaction_log.json"

def log_interaction(user_input: str, response: str):
    """
    Appends the user input and Gemini response to a local JSON log file.
    Args:
        user_input (str): The user's input message.
        response (str): The AI's response.
    """
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "user_input": user_input,
        "response": response
    }
    # Load existing log or start new
    if LOG_FILE.exists():
        with open(LOG_FILE, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []
    else:
        data = []
    data.append(entry)
    with open(LOG_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2) 