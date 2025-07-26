# Installation Guide

## Prerequisites
- Python 3.9 or higher
- pip (Python package installer)

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd LittleBits
```

### 2. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables
Create a `.env` file in the project root with:
```env
GEMINI_API_KEY=your_gemini_api_key_here
SECRET_KEY=your_secret_key_here
GOOGLE_CLIENT_ID=your_google_client_id_here
```

### 5. Initialize Database
```bash
python3 -m src.init_db
```

### 6. Run Database Migration (if updating existing database)
```bash
python3 src/migrate_db.py
```

### 7. Run the Application
```bash
uvicorn src.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation
Once running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Testing
```bash
pytest
```

## Project Structure
```
src/
├── main.py              # FastAPI application entry point
├── routers.py           # API route definitions
├── models.py            # SQLAlchemy database models
├── schemas.py           # Pydantic validation schemas
├── auth.py              # Authentication logic
├── database.py          # Database configuration
├── executor.py          # Gemini API integration
├── planner.py           # AI planning and memory
├── memory.py            # Interaction logging
├── external_tools.py    # Google Calendar/Fit integration
└── init_db.py           # Database initialization
```

## Key Features
- Google OAuth authentication
- AI-powered chat with Gemini
- Vector-based memory retrieval
- Cycle tracking and reminders
- Partner sharing features
- Google Calendar/Fit integration 