"""
main.py
FastAPI app for CycleWise backend.
"""

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from planner import plan_tasks
from executor import call_gemini
from memory import log_interaction
from fastapi.middleware.cors import CORSMiddleware
from routers import router as api_router
from database import get_db
import models
import auth
from sqlalchemy.orm import Session
import logging
from external_tools import CalendarTool, HealthTrackingTool, MedicalInfoTool
from planner import generate_contextual_response

logger = logging.getLogger(__name__)

app = FastAPI()

# Allow CORS for frontend dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

class GoogleToken(BaseModel):
    token: str

def agentic_fallback_response(user_input: str, user_id: int = 1, db: Session = None):
    """
    Fallback agentic response when Gemini API is unavailable.
    Directly uses external tools and generates contextual responses.
    """
    try:
        # Use external tools directly
        calendar_data = CalendarTool.get_user_schedule(user_id)
        health_data = HealthTrackingTool.get_health_data(user_id)
        sleep_data = HealthTrackingTool.get_sleep_data(user_id)
        medical_info = MedicalInfoTool.get_medical_info()
        
        # Generate contextual response
        response = generate_contextual_response(
            user_input, 
            calendar_data, 
            health_data, 
            sleep_data, 
            medical_info
        )
        
        return response
    except Exception as e:
        logger.error(f"Fallback response error: {e}")
        return "I'm here to help with your health and cycle tracking. What would you like to know?"

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
        try:
            gemini_response = call_gemini(enhanced_prompt)
        except Exception as e:
            logger.warning(f"Gemini API failed, using fallback: {e}")
            gemini_response = agentic_fallback_response(user_input, current_user.id, db)
        
        # Step 4: Log interaction with memory
        log_interaction(user_input, gemini_response, current_user.id, db)
        
        return ChatResponse(response=gemini_response)
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/demo/chat", response_model=ChatResponse)
def demo_chat_endpoint(request: ChatRequest):
    """
    Demo chat endpoint for unauthenticated testing.
    """
    user_input = request.message
    try:
        # Use fallback agentic response for demo
        response = agentic_fallback_response(user_input, user_id=1, db=None)
        return ChatResponse(response=response)
    except Exception as e:
        logger.error(f"Error in demo chat endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/chat", response_model=ChatResponse)
def api_chat_endpoint(request: ChatRequest, current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    """
    API chat endpoint for authenticated users.
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
        try:
            gemini_response = call_gemini(enhanced_prompt)
        except Exception as e:
            logger.warning(f"Gemini API failed, using fallback: {e}")
            gemini_response = agentic_fallback_response(user_input, current_user.id, db)
        
        # Step 4: Log interaction with memory
        log_interaction(user_input, gemini_response, current_user.id, db)
        
        return ChatResponse(response=gemini_response)
    except Exception as e:
        logger.error(f"Error in api chat endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/demo/auth", response_model=dict)
def demo_auth():
    """
    Demo authentication endpoint for testing.
    Returns a mock JWT token.
    """
    try:
        # Create a mock token for demo purposes
        mock_token = auth.create_access_token(data={"sub": "demo@example.com"})
        return {"access_token": mock_token, "token_type": "bearer"}
    except Exception as e:
        logger.error(f"Error in demo auth: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/auth/google", response_model=dict)
def google_login(payload: GoogleToken, db: Session = Depends(get_db)):
    """
    Google OAuth login endpoint.
    Verifies Google ID token and issues custom JWT.
    """
    try:
        # Verify Google token
        idinfo = auth.verify_google_token(payload.token)
        email = idinfo["email"]
        name = idinfo.get("name", "")
        
        # Get or create user
        user = auth.get_or_create_user(db, email, name)
        
        # Issue custom JWT
        access_token = auth.create_access_token(data={"sub": user.email})
        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        logger.error(f"Google login error: {e}")
        raise HTTPException(status_code=401, detail=str(e))

# Demo endpoints for health data
@app.get("/demo/health")
def demo_health():
    """Demo endpoint for health data."""
    from external_tools import HealthTrackingTool
    try:
        health_data = HealthTrackingTool.get_health_data(1)
        return {
            "success": True,
            "data": health_data,
            "user_id": 1
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "data": {
                "hydration": {"percentage": 75, "water_intake_ml": 1500, "recommended_ml": 2000, "status": "needs_improvement"},
                "exercise": {"steps_today": 6500, "calories_burned": 320, "active_minutes": 45, "status": "moderate"},
                "sleep": {"hours_last_night": 7.5, "quality_score": 8, "recommended_hours": 8, "status": "good"}
            }
        }

@app.get("/demo/calendar")
def demo_calendar():
    """Demo endpoint for calendar data."""
    from external_tools import CalendarTool
    try:
        calendar_data = CalendarTool.get_user_schedule(1)
        return {
            "success": True,
            "data": calendar_data,
            "user_id": 1
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "data": {
                "description": "3 meetings today, 2 hours total",
                "stress_level": "moderate",
                "meeting_count": 3,
                "total_hours": 2.0,
                "next_meeting": "2:00 PM",
                "free_time": "1:00 PM - 2:00 PM"
            }
        }

@app.get("/demo/weather")
def demo_weather():
    """Demo endpoint for weather data."""
    from external_tools import WeatherTool
    try:
        weather_data = WeatherTool.get_weather_data()
        return {
            "success": True,
            "data": weather_data,
            "user_id": 1
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "data": {
                "temperature": 72,
                "description": "Partly cloudy",
                "humidity": 65,
                "pressure": 1013,
                "impact_on_symptoms": "Moderate humidity may affect bloating and discomfort. Consider staying hydrated and avoiding salty foods."
            }
        }

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
