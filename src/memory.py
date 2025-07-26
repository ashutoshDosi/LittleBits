"""
memory.py
Logs user interactions to the database.
"""

import logging
from datetime import datetime
from sqlalchemy.orm import Session
from .models import Interaction

logger = logging.getLogger(__name__)

def log_interaction(
    user_input: str,
    response: str,
    user_id: int,
    db: Session,
    timestamp: datetime = None
) -> Interaction:
    """
    Logs the user input and AI response to the database.
    
    Args:
        user_input (str): The user's input message.
        response (str): The AI's response.
        user_id (int): The user's ID.
        db (Session): Database session.
        timestamp (datetime, optional): Optional timestamp (defaults to UTC now).
        
    Returns:
        Interaction: The newly logged interaction object.
    """
    try:
        interaction = Interaction(
            user_id=user_id,
            message=user_input.strip(),
            response=response.strip(),
            timestamp=timestamp or datetime.utcnow()
        )
        db.add(interaction)
        db.commit()
        db.refresh(interaction)
        logger.info(f"Logged interaction ID {interaction.id} for user {user_id}")
        return interaction
    except Exception as e:
        logger.exception("Error logging interaction")
        db.rollback()
        raise
