# 🌟 CycleWise - An Empathetic Menstrual Health Companion

**CycleWise** is an AI-powered menstrual health app that understands, predicts, and supports menstruators through their cycle — not just by tracking dates, but by having conversations about symptoms, emotions, and care.

## 🚀 Features

### ✅ **Implemented Features**
- **Conversational Symptom Tracker**: Log symptoms and moods with AI-powered insights
- **Cycle-Aware AI Companion**: Understands your cycle phases and provides personalized advice
- **Personalized Education**: Evidence-based information about menstrual health
- **Real-time Chat**: Powered by Google Gemini AI for empathetic conversations
- **Symptom & Mood Tracking**: Comprehensive logging with pattern recognition
- **Cycle Phase Detection**: Automatic phase calculation and insights
- **Partner Support**: Share cycle information with trusted partners
- **Health Correlations**: Integrates calendar, sleep, and weather data

### 🔄 **Agentic AI System**
- **ReAct Pattern**: Thought → Action → Observation → Reflection → Final Answer
- **Memory Retrieval**: Vector-based similarity search for personalized responses
- **External Tool Integration**: Calendar, health tracking, medical research, weather
- **Contextual Planning**: Multi-factor analysis for comprehensive recommendations

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - Database ORM
- **Google Gemini AI** - Conversational AI
- **JWT Authentication** - Secure user sessions
- **Google OAuth** - Social login integration

### Frontend
- **Next.js 15** - React framework with TypeScript
- **Tailwind CSS** - Modern styling
- **Lucide React** - Beautiful icons
- **NextAuth.js** - Authentication integration

### Database
- **SQLite** - Lightweight database (can be upgraded to PostgreSQL)

## 📋 Prerequisites

- **Python 3.9+**
- **Node.js 18+**
- **npm** or **yarn**
- **Google Gemini API Key** (free tier available)
- **Google OAuth Credentials** (optional, for social login)

## 🚀 Quick Start

### 1. **Clone the Repository**
```bash
git clone <repository-url>
cd CycleWise
```

### 2. **Set Up Environment Variables**
Create a `.env` file in the root directory:
```bash
# Gemini API Configuration
GEMINI_API_KEY=your_google_gemini_api_key_here

# JWT Secret Key (for authentication)
SECRET_KEY=your_secret_key_here_make_it_long_and_random

# Google OAuth Configuration (optional)
GOOGLE_CLIENT_ID=your_google_client_id_here
GOOGLE_CLIENT_SECRET=your_google_client_secret_here

# Database Configuration
DATABASE_URL=sqlite:///./cyclewise.db

# Server Configuration
HOST=0.0.0.0
PORT=8000
```

### 3. **Install Dependencies**

**Backend Dependencies:**
```bash
pip3 install -r requirements.txt
```

**Frontend Dependencies:**
```bash
cd src/frontend
npm install
cd ../..
```

### 4. **Initialize Database**
```bash
cd src
python3 -c "from database import engine; from models import Base; Base.metadata.create_all(bind=engine); print('Database initialized!')"
cd ..
```

### 5. **Start the Application**

**Option A: Use the Startup Script (Recommended)**
```bash
python3 start_app.py
```

**Option B: Start Manually**

Terminal 1 (Backend):
```bash
cd src
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Terminal 2 (Frontend):
```bash
cd src/frontend
npm run dev
```

### 6. **Access the Application**

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 🎯 How to Use

### **First Time Setup**
1. Open http://localhost:3000 in your browser
2. Click "Login" (demo mode available)
3. Set up your profile with age and cycle information
4. Start tracking your symptoms and moods

### **Daily Usage**
1. **View Today's Insights**: See your current cycle phase and recommendations
2. **Track Symptoms**: Log physical symptoms and emotional states
3. **Chat with AI**: Ask questions about your health, get personalized advice
4. **Learn**: Access educational content about menstrual health
5. **Partner Support**: Share information with trusted partners

### **AI Chat Examples**
- "I have cramps and feel tired today"
- "What should I eat during my period?"
- "I'm feeling moody and stressed"
- "How can I improve my sleep during my luteal phase?"

## 🔧 API Endpoints

### **Authentication**
- `POST /api/auth/google` - Google OAuth login
- `POST /demo/auth` - Demo authentication

### **User Management**
- `GET /api/me` - Get current user profile
- `PUT /api/me` - Update user profile
- `POST /api/users` - Create new user

### **Cycle Tracking**
- `POST /api/cycles` - Log cycle data
- `GET /api/cycles` - Get cycle history
- `GET /api/phase` - Get current cycle phase

### **Chat & AI**
- `POST /chat` - Authenticated chat with AI
- `POST /demo/chat` - Demo chat (no auth required)

### **Reminders**
- `POST /api/reminders` - Create reminder
- `GET /api/reminders` - Get user reminders

### **Partner Features**
- `POST /api/invite-partner` - Invite partner
- `GET /api/shared-info` - Get shared information

## 🏗️ Project Structure

```
CycleWise/
├── src/
│   ├── main.py              # FastAPI application
│   ├── models.py            # Database models
│   ├── auth.py              # Authentication utilities
│   ├── database.py          # Database configuration
│   ├── executor.py          # Gemini AI integration
│   ├── planner.py           # Agentic AI planner
│   ├── memory.py            # Memory management
│   ├── external_tools.py    # External API integrations
│   ├── routers.py           # API routes
│   ├── schemas.py           # Pydantic schemas
│   └── frontend/            # Next.js frontend
│       ├── src/
│       │   └── app/
│       │       ├── components/
│       │       ├── Chat/
│       │       ├── DayOverview/
│       │       ├── Learn/
│       │       └── PartnerTip/
│       └── package.json
├── requirements.txt         # Python dependencies
├── start_app.py            # Startup script
├── .env                    # Environment variables
└── README.md
```

## 🧪 Testing

### **Backend Tests**
```bash
cd src
python3 -m pytest test_*.py
```

### **Frontend Tests**
```bash
cd src/frontend
npm test
```

## 🔍 Troubleshooting

### **Common Issues**

1. **Import Errors**: Make sure you're running from the correct directory
2. **Database Errors**: Run the database initialization script
3. **API Key Issues**: Check your `.env` file and API key validity
4. **Port Conflicts**: Ensure ports 3000 and 8000 are available

### **Getting API Keys**

1. **Google Gemini API**:
   - Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create a new API key
   - Add to `.env` as `GEMINI_API_KEY`

2. **Google OAuth** (optional):
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create OAuth 2.0 credentials
   - Add to `.env` as `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Google Gemini AI** for providing the conversational AI capabilities
- **FastAPI** for the excellent web framework
- **Next.js** for the React framework
- **Tailwind CSS** for the beautiful styling

---

**Made with ❤️ for menstrual health awareness and support**


