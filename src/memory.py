"""
memory.py
Logs user interactions to a local JSON file.
"""

import json
from datetime import datetime
from pathlib import Path

LOG_FILE = Path(__file__).parent / "interaction_log.json"

def log_interaction(user_input: str, response: str, user_id: int, db: Session):
    """
    Logs the user input and AI response to the database.
    Validates non-empty input and response.
    """
    if not user_input or not response:
        raise ValueError("User input and response must not be empty.")
    try:
        new_interaction = Interaction(
            user_id=user_id,
            message=user_input,
            response=response,
            timestamp=datetime.utcnow()
        )
        db.add(new_interaction)
        db.commit()
        logger.info(f"Logged interaction for user {user_id}")
    except Exception as e:
        logger.error(f"Error logging interaction: {e}")
        db.rollback()
        raise 