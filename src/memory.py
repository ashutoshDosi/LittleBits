"""
memory.py
Memory management for CycleWise backend.
"""

import logging
from sqlalchemy.orm import Session
from database import get_db
import models
from datetime import datetime

logger = logging.getLogger(__name__)

def log_interaction(message: str, response: str, user_id: int, db: Session):
    """
    Log user interaction for memory retrieval.
    """
    try:
        interaction = models.Interaction(
            user_id=user_id,
            message=message,
            response=response,
            timestamp=datetime.utcnow()
        )
        db.add(interaction)
        db.commit()
        logger.info(f"Interaction logged for user {user_id}")
    except Exception as e:
        logger.error(f"Error logging interaction: {e}")
        db.rollback() 