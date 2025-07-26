"""
main.py
FastAPI app for CycleWise backend.
"""

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from .planner import plan_tasks, execute_action
from .executor import call_gemini
from .memory import log_interaction
from .external_tools import CalendarTool, HealthTrackingTool, MedicalInfoTool
from fastapi.middleware.cors import CORSMiddleware
from .routers import router as api_router
from . import models, auth
from .database import get_db
from sqlalchemy.orm import Session
import os
import logging

# Configure logging
logger = logging.getLogger(__name__)

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest, current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    """
    Enhanced chat endpoint with memory retrieval and ReAct pattern.
    Receives user message, retrieves memory, plans tasks using ReAct, calls Gemini, logs interaction, and returns response.
    """
    user_input = request.message
    try:
        # Step 1: Plan tasks using enhanced ReAct pattern with memory
        tasks = plan_tasks(user_input, user_id=current_user.id, db=db)
        
        # Step 2: Create enhanced prompt with task context
        task_context = "Planned tasks:\n"
        for task in tasks:
            task_context += f"- {task['task']} ({task['category']}): {task['reason']}\n"
        
        enhanced_prompt = f"""
Based on the user's input and planned tasks, provide a helpful response.

User Input: "{user_input}"

Planned Tasks:
{task_context}

Provide a comprehensive, helpful response that addresses the user's needs.
"""
        
        # Step 3: Call Gemini API with enhanced prompt
        gemini_response = call_gemini(enhanced_prompt)
        
        # Step 4: Log interaction with memory
        log_interaction(user_input, gemini_response, current_user.id, db)
        
        return ChatResponse(response=gemini_response)
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Demo mode for testing (remove in production)
@app.post("/demo/chat")
async def demo_chat_endpoint(request: ChatRequest):
    """
    Demo endpoint that bypasses authentication for testing.
    Uses the full ReAct agentic AI system with fallback.
    """
    try:
        # Step 1: Use the ReAct planner to analyze the request
        logger.info(f"Processing user request: {request.message}")
        
        try:
            # Try to use the full ReAct system with Gemini
            tasks = plan_tasks(request.message, "")
            logger.info(f"Generated {len(tasks)} tasks from ReAct planner")
            
            # Step 2: Execute tasks and gather context
            context_data = {}
            for task in tasks:
                try:
                    response = execute_action(task)
                    context_data[task.get('task', 'unknown')] = response
                    logger.info(f"Executed task: {task.get('task', 'unknown')}")
                except Exception as task_error:
                    logger.warning(f"Task execution failed: {task_error}")
                    context_data[task.get('task', 'unknown')] = f"Error: {task_error}"
            
            # Step 3: Generate response using Gemini with gathered context
            context_summary = "\n".join([f"{k}: {v}" for k, v in context_data.items()])
            prompt = f"""
            Based on the user's request and the gathered context, provide a comprehensive, evidence-based response.
            
            User Request: {request.message}
            
            Context from Analysis:
            {context_summary}
            
            Provide a helpful, compassionate response that:
            1. Addresses the user's specific concerns
            2. Incorporates the gathered health/calendar/medical data
            3. Offers evidence-based recommendations
            4. Suggests next steps or follow-up actions
            5. Maintains a supportive, professional tone
            """
            
            gemini_response = call_gemini(prompt)
            return ChatResponse(response=gemini_response)
            
        except Exception as gemini_error:
            logger.warning(f"Gemini API unavailable, using agentic fallback: {gemini_error}")
            
            # Fallback: Use the external tools directly in an agentic way
            return await agentic_fallback_response(request.message)
            
    except Exception as e:
        logger.error(f"Error in demo chat: {e}")
        return ChatResponse(response="I'm having trouble processing your request right now. Please try again later.")

async def agentic_fallback_response(user_message: str) -> ChatResponse:
    """
    Agentic fallback that uses external tools directly when Gemini is unavailable.
    This maintains the agentic architecture without relying on Gemini.
    """
    try:
        message_lower = user_message.lower()
        context_data = {}
        
        # Agentic analysis: Gather relevant data based on user input
        if any(word in message_lower for word in ['cramp', 'pain', 'tired', 'fatigue']):
            # Check health data for context
            try:
                health_data = HealthTrackingTool.get_health_data(1)
                context_data['health'] = health_data
                logger.info("Gathered health data for symptom analysis")
            except Exception as e:
                logger.warning(f"Health data gathering failed: {e}")
            
            # Get medical information
            try:
                medical_info = MedicalInfoTool.get_medical_info("cramps", "menstrual")
                context_data['medical'] = medical_info
                logger.info("Gathered medical information for cramps")
            except Exception as e:
                logger.warning(f"Medical info gathering failed: {e}")
        
        if any(word in message_lower for word in ['stress', 'busy', 'schedule', 'meeting']):
            # Check calendar for stress correlation
            try:
                calendar_data = CalendarTool.get_user_schedule(1)
                context_data['calendar'] = calendar_data
                logger.info("Gathered calendar data for stress analysis")
            except Exception as e:
                logger.warning(f"Calendar data gathering failed: {e}")
        
        if any(word in message_lower for word in ['eat', 'nutrition', 'food', 'diet']):
            # Get nutrition-specific medical info
            try:
                nutrition_info = MedicalInfoTool.get_medical_info("nutrition", "menstrual")
                context_data['nutrition'] = nutrition_info
                logger.info("Gathered nutrition information")
            except Exception as e:
                logger.warning(f"Nutrition info gathering failed: {e}")
        
        if any(word in message_lower for word in ['track', 'cycle', 'period', 'symptom']):
            # Get tracking-related information
            try:
                tracking_info = MedicalInfoTool.get_medical_info("tracking", "menstrual")
                context_data['tracking'] = tracking_info
                logger.info("Gathered tracking information")
            except Exception as e:
                logger.warning(f"Tracking info gathering failed: {e}")
        
        # Generate intelligent response based on gathered context
        response = generate_contextual_response(user_message, context_data)
        return ChatResponse(response=response)
        
    except Exception as e:
        logger.error(f"Error in agentic fallback: {e}")
        return ChatResponse(response="I'm having trouble processing your request right now. Please try again later.")

def generate_contextual_response(user_message: str, context_data: dict) -> str:
    """
    Generate an intelligent response based on gathered context data.
    This maintains the agentic approach by using the collected data.
    """
    message_lower = user_message.lower()
    
    # Build response based on available context
    response_parts = []
    
    # Add personalized greeting
    response_parts.append("Thank you for sharing that with me. Let me provide you with personalized, evidence-based recommendations based on your situation.")
    
    # Add context-specific information
    if 'health' in context_data:
        health = context_data['health']
        response_parts.append(f"\n📊 **Health Context**: I can see your current health status - hydration is at {health.get('hydration', {}).get('percentage', 'unknown')}%, and your sleep quality is {health.get('sleep', {}).get('status', 'unknown')}.")
    
    if 'calendar' in context_data:
        calendar = context_data['calendar']
        response_parts.append(f"\n📅 **Schedule Context**: Your calendar shows a stress level of {calendar.get('stress_level', 'unknown')} with {calendar.get('total_meetings', 0)} meetings today.")
    
    if 'medical' in context_data:
        medical = context_data['medical']
        if 'remedies' in medical:
            response_parts.append(f"\n🏥 **Medical Recommendations**: Based on medical research, here are evidence-based remedies:")
            for remedy in medical['remedies'][:3]:  # Top 3 remedies
                response_parts.append(f"• {remedy}")
    
    if 'nutrition' in context_data:
        nutrition = context_data['nutrition']
        if 'remedies' in nutrition:
            response_parts.append(f"\n🥗 **Nutrition Advice**: Here are evidence-based nutrition recommendations:")
            for remedy in nutrition['remedies'][:3]:  # Top 3 nutrition tips
                response_parts.append(f"• {remedy}")
    
    # Add specific recommendations based on user input
    if any(word in message_lower for word in ['cramp', 'pain']):
        response_parts.append("""
**For Your Cramps:**
• Apply heat therapy (heating pad or warm compress)
• Try gentle exercise like walking or stretching
• Consider over-the-counter pain relievers like ibuprofen
• Practice relaxation techniques to reduce muscle tension""")
    
    if any(word in message_lower for word in ['tired', 'fatigue']):
        response_parts.append("""
**For Your Fatigue:**
• Ensure adequate hydration (aim for 8-10 glasses of water daily)
• Get quality sleep (7-9 hours per night)
• Eat iron-rich foods to combat fatigue
• Consider gentle exercise to boost energy levels""")
    
    if any(word in message_lower for word in ['mood', 'bloat']):
        response_parts.append("""
**For Mood Changes & Bloating:**
• Practice stress-reduction techniques (deep breathing, meditation)
• Reduce salt intake to minimize bloating
• Eat smaller, more frequent meals
• Remember these changes are normal and temporary""")
    
    if any(word in message_lower for word in ['eat', 'nutrition']):
        response_parts.append("""
**Optimal Nutrition During Your Period:**
• Iron-rich foods: leafy greens, lean meats, legumes
• Omega-3 fatty acids: fish, nuts, seeds
• Complex carbohydrates: whole grains for steady energy
• Hydration: plenty of water and herbal teas
• Avoid: excess salt, caffeine, processed foods""")
    
    if any(word in message_lower for word in ['track', 'cycle']):
        response_parts.append("""
**Cycle Tracking Methods:**
• Symptom tracking: record daily symptoms, mood, energy
• Calendar method: mark period start/end dates
• Use menstrual health apps for comprehensive tracking
• Pay attention to physical signs (cervical mucus, temperature)
• Keep a detailed journal of your experiences""")
    
    # Add next steps
    response_parts.append("""
**Next Steps:**
• Would you like me to help you set up symptom tracking?
• Should I create reminders for self-care activities?
• Would you like to explore stress management techniques?
• Should I help you plan a nutrition strategy?

I'm here to support you throughout your menstrual health journey. What would be most helpful for you right now?""")
    
    return "\n".join(response_parts)

@app.post("/demo/auth")
async def demo_auth():
    """
    Demo authentication endpoint that returns a mock token.
    """
    return {"access_token": "demo_token_123", "token_type": "bearer"}

"""
How to run:
1. Create a .env file in the project root with:
   GEMINI_API_KEY=your_google_gemini_api_key_here
   SECRET_KEY=your_secret_key_here
   GOOGLE_CLIENT_ID=your_google_client_id_here
2. Install dependencies:
   pip install -r requirements.txt
3. Start the server:
   uvicorn src.main:app --reload
"""

from dotenv import load_dotenv
load_dotenv()

SECRET_KEY = os.environ["SECRET_KEY"]
