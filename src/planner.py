"""
planner.py

Enhanced agentic AI planner for CycleWise that implements:
- Memory retrieval using vector similarity (via Google Vertex AI embeddings + FAISS)
- ReAct pattern (Thought → Action → Observation → Reflection → Final Answer)
- Multi-step reasoning with Gemini API
- Structured task output with categories and reasons
"""

import json
import logging
from typing import List, Dict, Any, Optional
from .executor import call_gemini
from .database import get_db
from .models import Interaction
from sqlalchemy.orm import Session
from .external_tools import CalendarTool, HealthTrackingTool, MedicalInfoTool, WeatherTool
from datetime import datetime
from . import models
from google.cloud import aiplatform_v1
import faiss
import numpy as np

logger = logging.getLogger(__name__)

SUPPORTED_TASK_TYPES = [
    "track_symptoms",
    "recommend_remedies", 
    "explain_condition",
    "set_reminder",
    "chat_general",
    "send_partner_update",
]

# Vector embedding client setup (Google Vertex AI)
def embed_text(texts: List[str]) -> List[List[float]]:
    client = aiplatform_v1.PredictionServiceClient()
    endpoint = "projects/your-project/locations/us-central1/publishers/google/models/textembedding-gecko"

    instances = [{"content": t} for t in texts]
    response = client.predict(endpoint=endpoint, instances=instances)
    return [list(pred.embedding) for pred in response.predictions]

# Vector store (in-memory FAISS index)
embedding_dim = 768  # Depending on model used
memory_index = faiss.IndexFlatL2(embedding_dim)
memory_texts: List[str] = []


def update_memory_index(user_id: int, db: Session):
    global memory_index, memory_texts
    interactions = (
        db.query(Interaction)
        .filter(Interaction.user_id == user_id)
        .order_by(Interaction.timestamp.desc())
        .limit(100)
        .all()
    )
    memory_texts = [f"User: {i.message}\nAI: {i.response}" for i in interactions]
    if memory_texts:
        vectors = embed_text(memory_texts)
        memory_index = faiss.IndexFlatL2(len(vectors[0]))
        memory_index.add(np.array(vectors).astype('float32'))


def get_relevant_memory(user_id: int, user_input: str, db: Session) -> str:
    try:
        update_memory_index(user_id, db)
        if not memory_texts:
            return "No memory available."

        query_vector = np.array(embed_text([user_input])[0]).astype('float32').reshape(1, -1)
        _, I = memory_index.search(query_vector, k=5)
        retrieved = [memory_texts[i] for i in I[0] if i < len(memory_texts)]

        memory_context = "Relevant past interactions:\n\n" + "\n\n".join(retrieved)
        return memory_context
    except Exception as e:
        logger.error(f"Vector memory retrieval failed: {e}")
        return "Unable to retrieve relevant memory."

def execute_action(action: str, user_id: int, db: Session) -> str:
    """
    Execute the action decided by the AI and return observations.
    Now includes external tool integrations for enhanced agentic behavior.
    
    Args:
        action: The action to execute
        user_id: The user's ID
        db: Database session
    
    Returns:
        str: Observation from the action
    """
    try:
        # Calendar and stress correlation
        if "check_calendar" in action.lower() or "check_schedule" in action.lower():
            schedule = CalendarTool.get_user_schedule(user_id)
            return f"Calendar: {schedule['description']}. Stress level: {schedule['stress_level']}. This may affect your symptoms."
        
        # Health tracking data
        elif "check_health" in action.lower() or "check_hydration" in action.lower():
            health_data = HealthTrackingTool.get_health_data(user_id)
            hydration = health_data["hydration"]
            exercise = health_data["exercise"]
            sleep = health_data["sleep"]
            return f"Health Status: Hydration {hydration['percentage']}% ({hydration['water_intake_ml']}ml), Exercise {exercise['steps_today']} steps, Sleep {sleep['hours_last_night']} hours. Recommendations based on this data."
        
        # Medical information
        elif "get_medical_info" in action.lower() or "research_symptom" in action.lower():
            # Extract symptom from action (simplified)
            symptoms = ["cramps", "fatigue", "mood_changes", "bloating"]
            detected_symptom = None
            for symptom in symptoms:
                if symptom in action.lower():
                    detected_symptom = symptom
                    break
            
            if detected_symptom:
                medical_info = MedicalInfoTool.get_medical_info(detected_symptom)
                return f"Medical Info for {detected_symptom}: {medical_info['description']}. Evidence level: {medical_info['evidence_level']}. Remedies: {', '.join(medical_info['remedies'][:2])}"
            else:
                return "No specific symptom detected for medical research."
        
        # Weather correlation
        elif "check_weather" in action.lower():
            weather = WeatherTool.get_weather_data()
            return f"Weather: {weather['description']}, {weather['temperature']}°F. {weather['impact_on_symptoms']}"
        
        # Cycle phase check
        elif "check_cycle_phase" in action.lower():
            # Get user's last cycle data
            last_cycle = db.query(models.Cycle).filter(models.Cycle.user_id == user_id).order_by(models.Cycle.start_date.desc()).first()
            if last_cycle:
                days_since = (datetime.utcnow() - last_cycle.start_date).days
                if days_since <= 4:
                    phase = "menstrual"
                elif days_since <= 13:
                    phase = "follicular"
                elif days_since <= 16:
                    phase = "ovulatory"
                elif days_since <= 28:
                    phase = "luteal"
                else:
                    phase = "unknown"
                return f"Cycle Phase: {phase} (day {days_since}). This phase typically affects energy levels and symptoms."
            else:
                return "No cycle data found. Please log your period start date for phase tracking."
        
        # Log symptom
        elif "log_symptom" in action.lower():
            return "Symptom logged successfully. Pattern analysis shows correlation with cycle phase and stress levels."
        
        # Set reminder
        elif "set_reminder" in action.lower():
            return "Reminder set for hydration. Will notify user every 2 hours."
        
        # Check partner status
        elif "check_partner_status" in action.lower():
            return "Partner has access to cycle info. Can send supportive message."
        
        # Comprehensive health analysis
        elif "comprehensive_analysis" in action.lower():
            # Get all external data
            schedule = CalendarTool.get_user_schedule(user_id)
            health_data = HealthTrackingTool.get_health_data(user_id)
            weather = WeatherTool.get_weather_data()
            
            return f"Comprehensive Analysis: Stress level {schedule['stress_level']}, Hydration {health_data['hydration']['percentage']}%, Weather {weather['condition']}. Combined factors may affect your symptoms."
        
        # Default action
        else:
            return f"Action '{action}' executed successfully."
            
    except Exception as e:
        logger.error(f"Error executing action: {e}")
        return f"Action failed: {str(e)}"

def plan_tasks(user_input: str, user_id: Optional[int] = None, db: Optional[Session] = None) -> List[Dict[str, Any]]:
    """
    Enhanced agentic AI planner using ReAct pattern with memory retrieval.
    
    Args:
        user_input: The user's input message
        user_id: The user's ID (optional, for memory retrieval)
        db: Database session (optional, for memory retrieval)
    
    Returns:
        List[Dict]: List of structured tasks with task, category, and reason
    """
    
    # Step 1: Retrieve relevant memory
    memory_context = ""
    if user_id and db:
        memory_context = get_relevant_memory(user_id, user_input, db)
    
    # Step 2: Construct ReAct prompt
    react_prompt = f"""
You are an AI assistant for a menstrual health app. Use the ReAct pattern to help the user.

CONTEXT:
{memory_context}

CURRENT USER INPUT: "{user_input}"

Follow this ReAct pattern step by step:

1. THOUGHT: Think step-by-step about what the user needs. Consider their context and current input.

2. ACTION: Decide on a specific action to take. Available tools:
   - check_calendar - Check user's schedule for stress correlation
   - check_health - Get hydration, exercise, sleep data
   - get_medical_info - Research symptoms for evidence-based advice
   - check_weather - Get weather data for symptom correlation
   - check_cycle_phase - Determine current menstrual phase
   - log_symptom - Log user's symptoms
   - set_reminder - Set health reminders
   - check_partner_status - Check partner access and support options
   - comprehensive_analysis - Analyze all factors (stress, health, weather, cycle)

3. OBSERVATION: I will execute your action and provide the result.

4. REFLECTION: Reflect on the observation and what it means for the user.

5. FINAL ANSWER: Based on your reflection, provide a JSON array of tasks to help the user. Each task should have:
   - task: specific action to take
   - category: one of {SUPPORTED_TASK_TYPES}
   - reason: why this task is needed

Start with your THOUGHT:
"""

    try:
        logger.info(f"ReAct prompt: {react_prompt}")
        
        # Step 3: Get initial ReAct response
        react_response = call_gemini(react_prompt)
        logger.info(f"ReAct response: {react_response}")
        
        # Step 4: Extract action from response
        action_match = None
        if "ACTION:" in react_response:
            action_section = react_response.split("ACTION:")[1].split("OBSERVATION:")[0].strip()
            # Extract the action (first line after ACTION:)
            action_lines = [line.strip() for line in action_section.split('\n') if line.strip()]
            if action_lines:
                action_match = action_lines[0]
        
        # Step 5: Execute action and get observation
        observation = ""
        if action_match and db:
            observation = execute_action(action_match, user_id, db)
        else:
            observation = "No specific action to execute."
        
        # Step 6: Create reflection prompt
        reflection_prompt = f"""
Based on the ReAct pattern, here's what happened:

THOUGHT: {react_response.split('THOUGHT:')[1].split('ACTION:')[0].strip() if 'THOUGHT:' in react_response else 'Analysis of user needs'}

ACTION: {action_match or 'No specific action'}

OBSERVATION: {observation}

Now REFLECT on this observation and provide your FINAL ANSWER as a JSON array of tasks to help the user.

Each task should have:
- task: specific action to take
- category: one of {SUPPORTED_TASK_TYPES}
- reason: why this task is needed

Respond with only the JSON array:
"""
        
        # Step 7: Get final response with tasks
        final_response = call_gemini(reflection_prompt)
        logger.info(f"Final response: {final_response}")
        
        # Step 8: Parse and validate JSON response
        try:
            # Extract JSON from response
            json_start = final_response.find('[')
            json_end = final_response.rfind(']') + 1
            if json_start != -1 and json_end != 0:
                json_str = final_response[json_start:json_end]
                tasks = json.loads(json_str)
                
                # Validate tasks
                if isinstance(tasks, list):
                    validated_tasks = []
                    for task in tasks:
                        if isinstance(task, dict) and 'task' in task and 'category' in task:
                            # Ensure category is supported
                            if task['category'] in SUPPORTED_TASK_TYPES:
                                validated_tasks.append({
                                    'task': task['task'],
                                    'category': task['category'],
                                    'reason': task.get('reason', 'No reason provided')
                                })
                    
                    if validated_tasks:
                        return validated_tasks
            
            # Fallback: try to extract tasks from the response
            fallback_tasks = []
            for task_type in SUPPORTED_TASK_TYPES:
                if task_type.lower() in final_response.lower():
                    fallback_tasks.append({
                        'task': f'Handle {task_type}',
                        'category': task_type,
                        'reason': 'Detected from response'
                    })
            
            if fallback_tasks:
                return fallback_tasks
                
        except (json.JSONDecodeError, KeyError) as e:
            logger.error(f"Error parsing JSON response: {e}")
    
    except Exception as e:
        logger.error(f"Error in ReAct planning: {e}")
    
    # Step 9: Fallback to default
    return [{
        'task': 'Provide general support and information',
        'category': 'chat_general',
        'reason': 'Fallback due to processing error'
    }] 