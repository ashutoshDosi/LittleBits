"""
main.py
FastAPI app for CycleWise backend.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .planner import plan_tasks
from .executor import call_gemini
from .memory import log_interaction
from fastapi.middleware.cors import CORSMiddleware
from .routers import router as api_router
import os

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
def chat_endpoint(request: ChatRequest):
    """
    Receives user message, plans tasks, calls Gemini, logs interaction, and returns response.
    """
    user_input = request.message
    try:
        # Plan tasks (stub logic)
        tasks = plan_tasks(user_input)
        # For now, just join tasks for Gemini prompt
        prompt = "\n".join(tasks)
        # Call Gemini API
        gemini_response = call_gemini(prompt)
        # Log interaction
        log_interaction(user_input, gemini_response)
        return ChatResponse(response=gemini_response)
    except Exception as e:
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

from dotenv import load_dotenv
load_dotenv()

SECRET_KEY = os.environ["SECRET_KEY"]
