"""
main.py
FastAPI app for CycleWise backend.
"""

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from .planner import plan_tasks
from .executor import call_gemini
from .memory import log_interaction
from fastapi.middleware.cors import CORSMiddleware
from .routers import router as api_router
from .database import get_db
from . import models
from . import auth
from sqlalchemy.orm import Session
import logging

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
        log_interaction(user_input, gemini_response)
        
        return ChatResponse(response=gemini_response)
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))

"""
How to run:
1. Create a .env file in the project root with:
   GEMINI_API_KEY=your_google_gemini_api_key_here
2. Install dependencies:
   pip install -r requirements.txt
3. Start the server:
   uvicorn src.main:app --reload
"""
