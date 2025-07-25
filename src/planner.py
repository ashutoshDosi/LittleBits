"""
planner.py
Stub logic for planning tasks from user input.
"""

def plan_tasks(user_input: str) -> list[str]:
    """
    Splits the user input into 2-3 sub-tasks (stub logic).
    Args:
        user_input (str): The user's input message.
    Returns:
        list[str]: List of sub-task strings.
    """
    # For now, just split the input into sentences or chunks (stub logic)
    # In a real implementation, this would use NLP or LLMs
    parts = [s.strip() for s in user_input.replace('?', '.').split('.') if s.strip()]
    # Return up to 3 sub-tasks
    return parts[:3] 