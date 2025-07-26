"""
routers.py
API routes for CycleWise backend.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models
import auth
import schemas
from datetime import datetime
from typing import List

router = APIRouter()

# --- User Management ---
@router.post("/users", response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    db_user = models.User(
        email=user.email,
        age=user.age,
        cycle_start_date=user.cycle_start_date,
        period_duration=user.period_duration
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/me", response_model=schemas.UserOut)
def get_current_user(current_user: models.User = Depends(auth.get_current_user)):
    return current_user

@router.put("/me", response_model=schemas.UserOut)
def update_user(
    user_update: schemas.UserUpdate,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    if user_update.age is not None:
        current_user.age = user_update.age
    if user_update.cycle_start_date is not None:
        current_user.cycle_start_date = user_update.cycle_start_date
    if user_update.period_duration is not None:
        current_user.period_duration = user_update.period_duration
    
    db.commit()
    db.refresh(current_user)
    return current_user

# --- Cycle/Phase Management ---
@router.post("/cycles", response_model=schemas.CycleOut)
def log_cycle(
    cycle: schemas.CycleCreate,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db),
):
    new_cycle = models.Cycle(
        user_id=current_user.id,
        start_date=cycle.start_date,
        symptoms=cycle.symptoms,
        moods=cycle.moods,
    )
    db.add(new_cycle)
    db.commit()
    db.refresh(new_cycle)
    return new_cycle

@router.get("/cycles", response_model=List[schemas.CycleOut])
def get_cycles(
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    cycles = db.query(models.Cycle).filter(models.Cycle.user_id == current_user.id).all()
    return cycles

@router.get("/phase")
def get_current_phase(
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db),
):
    last_cycle = db.query(models.Cycle).filter(models.Cycle.user_id == current_user.id).order_by(models.Cycle.start_date.desc()).first()
    if not last_cycle:
        return {"phase": None, "message": "No cycle data found."}
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
    return {"phase": phase, "days_since": days_since}

# --- Reminders ---
@router.post("/reminders", response_model=schemas.ReminderOut)
def create_reminder(
    reminder: schemas.ReminderCreate,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    new_reminder = models.Reminder(
        user_id=current_user.id,
        type=reminder.type,
        time=reminder.time,
        method=reminder.method
    )
    db.add(new_reminder)
    db.commit()
    db.refresh(new_reminder)
    return new_reminder

@router.get("/reminders", response_model=List[schemas.ReminderOut])
def get_reminders(
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    reminders = db.query(models.Reminder).filter(models.Reminder.user_id == current_user.id).all()
    return reminders

# --- Partner Features ---
@router.post("/invite-partner")
def invite_partner(
    partner_email: str,
    consent_type: str = "cycle",
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    # Find partner user
    partner_user = db.query(models.User).filter(models.User.email == partner_email).first()
    if not partner_user:
        raise HTTPException(status_code=404, detail="Partner user not found")
    
    # Check if invitation already exists
    existing_invite = db.query(models.Partner).filter(
        models.Partner.user_id == current_user.id,
        models.Partner.partner_user_id == partner_user.id
    ).first()
    
    if existing_invite:
        raise HTTPException(status_code=400, detail="Invitation already sent")
    
    # Create partner relationship
    partner_relation = models.Partner(
        user_id=current_user.id,
        partner_user_id=partner_user.id,
        consent_type=consent_type,
        status="pending"
    )
    db.add(partner_relation)
    db.commit()
    
    return {"message": f"Invitation sent to {partner_email}"}

@router.get("/shared-info")
def get_shared_info(
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db),
):
    # Show info shared with the current user as a partner
    partner_links = db.query(models.Partner).filter(models.Partner.partner_user_id == current_user.id, models.Partner.status == "accepted").all()
    shared = []
    for link in partner_links:
        owner = db.query(models.User).filter(models.User.id == link.user_id).first()
        if link.consent_type == "cycle":
            cycles = db.query(models.Cycle).filter(models.Cycle.user_id == owner.id).all()
            shared.append({
                "owner": owner.email,
                "cycles": [
                    {
                        "start_date": c.start_date.isoformat(),
                        "symptoms": c.symptoms,
                        "moods": c.moods
                    } for c in cycles
                ]
            })
        # Add more types as needed
    return shared

# --- Health & External Data ---
@router.get("/health")
def get_health_data(
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    """Get comprehensive health data including hydration, exercise, and sleep."""
    from external_tools import HealthTrackingTool
    
    try:
        health_data = HealthTrackingTool.get_health_data(current_user.id)
        return {
            "success": True,
            "data": health_data,
            "user_id": current_user.id
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

@router.get("/calendar")
def get_calendar_data(
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    """Get calendar data and stress analysis."""
    from external_tools import CalendarTool
    
    try:
        calendar_data = CalendarTool.get_user_schedule(current_user.id)
        return {
            "success": True,
            "data": calendar_data,
            "user_id": current_user.id
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

@router.get("/weather")
def get_weather_data(
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    """Get weather data and its impact on symptoms."""
    from external_tools import WeatherTool
    
    try:
        weather_data = WeatherTool.get_weather_data()
        return {
            "success": True,
            "data": weather_data,
            "user_id": current_user.id
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

@router.get("/health/insights")
def get_health_insights(
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    """Get AI-powered health insights based on current data."""
    from external_tools import HealthTrackingTool, CalendarTool, WeatherTool
    
    try:
        # Gather all data
        health_data = HealthTrackingTool.get_health_data(current_user.id)
        calendar_data = CalendarTool.get_user_schedule(current_user.id)
        weather_data = WeatherTool.get_weather_data()
        
        # Get current phase
        last_cycle = db.query(models.Cycle).filter(models.Cycle.user_id == current_user.id).order_by(models.Cycle.start_date.desc()).first()
        days_since = (datetime.utcnow() - last_cycle.start_date).days if last_cycle else 0
        
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
        
        # Generate insights
        insights = {
            "phase": phase,
            "recommendations": [],
            "focus_areas": [],
            "correlations": []
        }
        
        # Hydration insights
        if health_data["hydration"]["percentage"] < 80:
            insights["recommendations"].append("Increase water intake by 500ml today")
            insights["focus_areas"].append("hydration")
        
        # Exercise insights
        if health_data["exercise"]["steps_today"] < 8000:
            insights["recommendations"].append("Take a 15-minute walk during your free time")
            insights["focus_areas"].append("activity")
        
        # Sleep insights
        if health_data["sleep"]["hours_last_night"] < 7:
            insights["recommendations"].append("Prioritize getting 8 hours of sleep tonight")
            insights["focus_areas"].append("sleep")
        
        # Calendar stress insights
        if calendar_data["stress_level"] == "high":
            insights["recommendations"].append("Practice stress management between meetings")
            insights["focus_areas"].append("stress_management")
        
        # Weather correlations
        if weather_data["humidity"] > 60:
            insights["correlations"].append("High humidity may affect bloating - stay hydrated")
        
        # Phase-specific insights
        if phase == "luteal":
            insights["recommendations"].append("This is your luteal phase - prioritize rest and self-care")
        elif phase == "menstrual":
            insights["recommendations"].append("During your period - be gentle with yourself and rest as needed")
        
        return {
            "success": True,
            "insights": insights,
            "data": {
                "health": health_data,
                "calendar": calendar_data,
                "weather": weather_data
            }
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "insights": {
                "phase": "unknown",
                "recommendations": ["Stay hydrated", "Get adequate sleep", "Practice self-care"],
                "focus_areas": ["general_wellness"],
                "correlations": []
            }
        }
