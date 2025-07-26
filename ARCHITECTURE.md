# 🏗️ CycleWise Architecture

## System Overview

CycleWise is an **Agentic AI** application that follows the **ReAct pattern** (Reasoning + Acting) to provide empathetic menstrual health support. The system integrates multiple external tools and APIs to deliver personalized, context-aware responses.

## Core Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              CYCLEWISE SYSTEM                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐         │
│  │   FRONTEND      │    │    BACKEND      │    │   EXTERNAL      │         │
│  │   (Next.js)     │    │   (FastAPI)     │    │     APIS        │         │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘         │
│           │                       │                       │                 │
│           │                       │                       │                 │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐         │
│  │   React UI      │    │   Agentic AI    │    │  Google Gemini  │         │
│  │   Components    │◄──►│    Engine       │◄──►│      API        │         │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘         │
│           │                       │                       │                 │
│           │                       │                       │                 │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐         │
│  │   State Mgmt    │    │   Memory Store  │    │  Google Calendar│         │
│  │   (LocalStorage)│    │   (SQLite)      │    │      API        │         │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘         │
│           │                       │                       │                 │
│           │                       │                       │                 │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐         │
│  │   Auth System   │    │   External      │    │  Weather API    │         │
│  │   (JWT/OAuth)   │    │   Tools         │    │   (Mock)        │         │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘         │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Agentic AI Workflow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           REACT PATTERN WORKFLOW                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  1. RECEIVE INPUT                                                           │
│     ┌─────────────────┐                                                    │
│     │ User Message    │                                                    │
│     │ "I have cramps" │                                                    │
│     └─────────────────┘                                                    │
│              │                                                              │
│              ▼                                                              │
│                                                                             │
│  2. MEMORY RETRIEVAL                                                        │
│     ┌─────────────────┐                                                    │
│     │ Vector Search   │                                                    │
│     │ Past Symptoms   │                                                    │
│     │ Cycle History   │                                                    │
│     └─────────────────┘                                                    │
│              │                                                              │
│              ▼                                                              │
│                                                                             │
│  3. PLANNING (ReAct)                                                        │
│     ┌─────────────────┐                                                    │
│     │ Thought:        │                                                    │
│     │ "User has cramps│                                                    │
│     │  in luteal phase│                                                    │
│     │  - check cycle  │                                                    │
│     │  - get remedies │                                                    │
│     │  - suggest care"│                                                    │
│     └─────────────────┘                                                    │
│              │                                                              │
│              ▼                                                              │
│                                                                             │
│  4. ACTION (Tool Calls)                                                     │
│     ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐      │
│     │ Medical Info    │    │ Cycle Phase     │    │ Health Data     │      │
│     │ Tool            │    │ Calculator      │    │ Analysis        │      │
│     └─────────────────┘    └─────────────────┘    └─────────────────┘      │
│              │                       │                       │              │
│              ▼                       ▼                       ▼              │
│                                                                             │
│  5. OBSERVATION                                                            │
│     ┌─────────────────┐                                                    │
│     │ Tool Results    │                                                    │
│     │ - Remedies      │                                                    │
│     │ - Phase Info    │                                                    │
│     │ - Health Status │                                                    │
│     └─────────────────┘                                                    │
│              │                                                              │
│              ▼                                                              │
│                                                                             │
│  6. REFLECTION                                                              │
│     ┌─────────────────┐                                                    │
│     │ Context Analysis│                                                    │
│     │ - Phase-aware   │                                                    │
│     │ - Personalized  │                                                    │
│     │ - Empathetic    │                                                    │
│     └─────────────────┘                                                    │
│              │                                                              │
│              ▼                                                              │
│                                                                             │
│  7. FINAL RESPONSE                                                          │
│     ┌─────────────────┐                                                    │
│     │ Gemini AI       │                                                    │
│     │ Response        │                                                    │
│     │ + Memory Log    │                                                    │
│     └─────────────────┘                                                    │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Core Modules

### 1. Planner (`planner.py`)
**Purpose**: Break down user goals into sub-tasks using ReAct pattern

```python
def plan_tasks(user_input: str, user_id: int, db: Session) -> List[Dict]:
    """
    ReAct Pattern Implementation:
    1. THOUGHT: Analyze user input and context
    2. ACTION: Plan specific tasks
    3. OBSERVATION: Consider available tools
    4. REFLECTION: Determine optimal approach
    """
```

**Key Features**:
- **Context Analysis**: Understands cycle phases, symptoms, moods
- **Task Decomposition**: Breaks complex requests into actionable steps
- **Tool Selection**: Chooses appropriate external tools
- **Priority Ranking**: Orders tasks by importance and urgency

### 2. Executor (`executor.py`)
**Purpose**: Logic for calling LLMs (Gemini API) and external tools

```python
def call_gemini(prompt: str) -> str:
    """
    Gemini API Integration:
    - Handles API authentication
    - Manages rate limiting
    - Implements fallback strategies
    - Processes responses
    """
```

**Key Features**:
- **Gemini API Integration**: Primary LLM for conversations
- **Error Handling**: Graceful fallbacks and retries
- **Response Processing**: Context-aware response generation
- **Tool Orchestration**: Coordinates multiple external APIs

### 3. Memory (`memory.py`)
**Purpose**: Log and store memory for personalized responses

```python
def log_interaction(user_id: int, input_text: str, response: str, db: Session):
    """
    Memory Management:
    - Stores user interactions
    - Implements vector similarity search
    - Enables context retrieval
    - Maintains conversation history
    """
```

**Key Features**:
- **Vector Embeddings**: Uses Google Vertex AI for similarity search
- **FAISS Integration**: Fast similarity search for memory retrieval
- **Contextual Memory**: Stores cycle phases, symptoms, moods
- **Personalization**: Enables tailored responses based on history

## External Tool Integration

### 1. Google Calendar API
```python
class CalendarTool:
    def get_calendar_data(access_token: str) -> Dict:
        """
        Real Google Calendar Integration:
        - Fetches actual calendar events
        - Calculates meeting stress levels
        - Correlates with cycle symptoms
        """
```

### 2. Health Tracking (Mock → Google Fit)
```python
class HealthTrackingTool:
    def get_health_data(user_id: int) -> Dict:
        """
        Health Data Integration:
        - Hydration tracking
        - Exercise metrics
        - Sleep quality
        - Cycle correlations
        """
```

### 3. Medical Information Database
```python
class MedicalInfoTool:
    def get_medical_info(symptom: str) -> Dict:
        """
        Evidence-Based Medical Info:
        - Symptom research
        - Remedy suggestions
        - When to see doctor
        - Cycle-specific advice
        """
```

### 4. Weather API (Mock → Real)
```python
class WeatherTool:
    def get_weather_data() -> Dict:
        """
        Weather Correlation:
        - Temperature impact
        - Humidity effects
        - Symptom correlations
        - Environmental factors
        """
```

## Data Flow Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   User Input    │───►│   Frontend      │───►│   Backend API   │
│   (Browser)     │    │   (Next.js)     │    │   (FastAPI)     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │                       │
                                ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   State Mgmt    │    │   Agentic AI    │    │   Database      │
│   (LocalStorage)│    │   Engine        │    │   (SQLite)      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │                       │
                                ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   UI Updates    │◄───│   Gemini API    │◄───│   Memory Store  │
│   (React)       │    │   Response      │    │   (Vector DB)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Security Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              SECURITY LAYERS                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐         │
│  │   Frontend      │    │   API Gateway   │    │   Backend       │         │
│  │   Security      │    │   Security      │    │   Security      │         │
│  │                 │    │                 │    │                 │         │
│  │ • HTTPS Only    │    │ • CORS Policy   │    │ • JWT Auth      │         │
│  │ • Input Val.    │    │ • Rate Limiting │    │ • OAuth 2.0     │         │
│  │ • XSS Protection│    │ • API Keys      │    │ • SQL Injection │         │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘         │
│                                                                             │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐         │
│  │   Data Storage  │    │   API Keys      │    │   Environment   │         │
│  │   Security      │    │   Management    │    │   Security      │         │
│  │                 │    │                 │    │                 │         │
│  │ • SQLite        │    │ • .env Files    │    │ • No Secrets    │         │
│  │ • Encryption    │    │ • Git Ignore    │    │ • Secure Config │         │
│  │ • Access Control│    │ • Key Rotation  │    │ • Prod Ready    │         │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘         │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Scalability Considerations

### Current Implementation
- **SQLite Database**: Lightweight, suitable for development
- **In-Memory Processing**: Fast response times
- **Single Instance**: Simple deployment

### Production Scalability
- **PostgreSQL**: For production database
- **Redis**: For caching and session management
- **Load Balancing**: Multiple backend instances
- **CDN**: For static assets
- **Microservices**: Separate services for different features

## Monitoring & Observability

### Logging Strategy
```python
# Structured logging for all operations
logger.info("User interaction", extra={
    "user_id": user_id,
    "action": "symptom_logging",
    "cycle_phase": current_phase,
    "response_time": response_time
})
```

### Metrics Collection
- **API Response Times**: Monitor performance
- **Error Rates**: Track system health
- **User Engagement**: Feature usage analytics
- **Memory Usage**: System resource monitoring

### Health Checks
- **Database Connectivity**: Ensure data access
- **External API Status**: Monitor dependencies
- **Memory Store Health**: Vector database status
- **Gemini API Status**: LLM service availability

## Deployment Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           DEPLOYMENT ARCHITECTURE                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐         │
│  │   Load Balancer │    │   Web Server    │    │   Application   │         │
│  │   (Nginx)       │    │   (Gunicorn)    │    │   (FastAPI)     │         │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘         │
│           │                       │                       │                 │
│           ▼                       ▼                       ▼                 │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐         │
│  │   Static Files  │    │   Process Mgmt  │    │   Database      │         │
│  │   (Next.js)     │    │   (PM2)         │    │   (SQLite/PostgreSQL)     │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘         │
│                                                                             │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐         │
│  │   Environment   │    │   Monitoring    │    │   Backup        │         │
│  │   Variables     │    │   (Prometheus)  │    │   (Automated)   │         │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘         │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Future Enhancements

### Phase 2 Features
- **Real Google Fit Integration**: Actual health data
- **Weather API Integration**: Real weather data
- **Machine Learning**: Predictive cycle analysis
- **Mobile App**: React Native implementation

### Advanced AI Features
- **Multi-Modal AI**: Image analysis for symptoms
- **Predictive Analytics**: Cycle prediction models
- **Natural Language Processing**: Advanced conversation understanding
- **Personalized Recommendations**: ML-based suggestions

---

**Architecture designed for scalability, security, and user privacy while maintaining the empathetic, supportive nature of CycleWise.**

