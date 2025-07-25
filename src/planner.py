"""
planner.py

This module provides the plan_tasks function, which uses the Google Gemini API (via call_gemini from executor.py)
to classify user input into one or more supported task types for the CycleWise app.

Supported task types:
1. track_symptoms – track the user’s mood, pain, or cycle symptoms.
2. recommend_remedies – suggest natural or medical ways to ease symptoms.
3. explain_condition – explain PMS, PCOS, cramps, etc.
4. set_reminder – schedule a reminder.
5. chat_general – casual conversation or general info.
6. send_partner_update – write a message to the user’s partner explaining how they’re feeling and how to support them.
"""

import json
import logging
from typing import List
from .executor import call_gemini

logger = logging.getLogger(__name__)

SUPPORTED_TASK_TYPES = [
    "track_symptoms",
    "recommend_remedies",
    "explain_condition",
    "set_reminder",
    "chat_general",
    "send_partner_update",
]

def plan_tasks(user_input: str) -> List[str]:
    """
    Classify user input into one or more supported task types using Gemini.

    Args:
        user_input (str): The user's input message.
    Returns:
        List[str]: List of matching task type strings.
    """
    prompt = (
        "You are an AI assistant for a menstrual health app. "
        "Classify the following user input into one or more of these task types, "
        "returning a JSON array of the matching types (use only these exact strings):\n"
        "1. track_symptoms – track the user’s mood, pain, or cycle symptoms.\n"
        "2. recommend_remedies – suggest natural or medical ways to ease symptoms.\n"
        "3. explain_condition – explain PMS, PCOS, cramps, etc.\n"
        "4. set_reminder – schedule a reminder.\n"
        "5. chat_general – casual conversation or general info.\n"
        "6. send_partner_update – write a message to the user’s partner explaining how they’re feeling and how to support them.\n"
        "\nUser input: '" + user_input + "'\n"
        "Respond ONLY with a JSON array of one or more matching task type strings."
    )
    try:
        logger.info(f"Gemini prompt: {prompt}")
        response = call_gemini(prompt)
        logger.info(f"Gemini response: {response}")
        # Try to parse the response as JSON
        tasks = json.loads(response)
        if not isinstance(tasks, list) or not all(isinstance(t, str) for t in tasks):
            raise ValueError("Response is not a JSON array of strings.")
        # Optionally, filter to only supported types
        tasks = [t for t in tasks if t in SUPPORTED_TASK_TYPES]
        if not tasks:
            return ["chat_general"]
        return tasks
    except Exception as e:
        logger.error(f"Failed to classify tasks with Gemini: {e}")
        return ["chat_general"] 