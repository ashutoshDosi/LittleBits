"""
external_tools.py

External tool integrations for CycleWise agentic AI:
- Google Calendar API for stress correlation
- Google Fit API for health tracking (hydration, exercise, sleep)

Note: Requires Google Cloud Console setup with Calendar and Fitness APIs enabled.
"""

import requests
import logging
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import os

logger = logging.getLogger(__name__)

# Google API configurations
GOOGLE_CALENDAR_API_KEY = os.getenv("GOOGLE_CALENDAR_API_KEY")
GOOGLE_FIT_API_KEY = os.getenv("GOOGLE_FIT_API_KEY")
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")

class CalendarTool:
    """Google Calendar integration for stress correlation."""
    
    @staticmethod
    def get_user_schedule(user_id: int, date: str = None, access_token: str = None) -> Dict[str, Any]:
        """
        Get user's Google Calendar schedule for stress correlation.
        
        Args:
            user_id: User ID
            date: Date to check (default: today)
            access_token: Google OAuth access token
        
        Returns:
            Dict with schedule information
        """
        try:
            if date is None:
                date = datetime.now().strftime("%Y-%m-%d")
            
            if not access_token:
                logger.warning("No access token provided for Google Calendar")
                return CalendarTool._get_fallback_schedule(date)
            
            # Create credentials from access token
            credentials = Credentials(
                token=access_token,
                client_id=GOOGLE_CLIENT_ID,
                client_secret=GOOGLE_CLIENT_SECRET,
                token_uri="https://oauth2.googleapis.com/token"
            )
            
            # Build Calendar service
            service = build('calendar', 'v3', credentials=credentials)
            
            # Get calendar events for the specified date
            start_time = f"{date}T00:00:00Z"
            end_time = f"{date}T23:59:59Z"
            
            events_result = service.events().list(
                calendarId='primary',
                timeMin=start_time,
                timeMax=end_time,
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            events = events_result.get('items', [])
            
            # Analyze schedule for stress correlation
            total_meetings = len([e for e in events if e.get('eventType') == 'default'])
            total_hours = 0
            event_details = []
            
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                end = event['end'].get('dateTime', event['end'].get('date'))
                
                if start and end and 'T' in start and 'T' in end:
                    start_dt = datetime.fromisoformat(start.replace('Z', '+00:00'))
                    end_dt = datetime.fromisoformat(end.replace('Z', '+00:00'))
                    duration = (end_dt - start_dt).total_seconds() / 3600
                    total_hours += duration
                    
                    event_details.append({
                        "time": start_dt.strftime("%I:%M %p"),
                        "title": event.get('summary', 'No title'),
                        "duration": int(duration * 60)  # Convert to minutes
                    })
            
            # Determine stress level based on schedule
            if total_meetings >= 6 or total_hours >= 10:
                stress_level = "high"
                description = f"Very busy day with {total_meetings} meetings and {total_hours:.1f} hours of commitments"
            elif total_meetings >= 3 or total_hours >= 7:
                stress_level = "medium"
                description = f"Moderate day with {total_meetings} meetings and {total_hours:.1f} hours of commitments"
            else:
                stress_level = "low"
                description = f"Light day with {total_meetings} meetings and {total_hours:.1f} hours of commitments"
            
            schedule_data = {
                "date": date,
                "meetings": total_meetings,
                "total_hours": round(total_hours, 1),
                "stress_level": stress_level,
                "description": description,
                "events": event_details
            }
            
            logger.info(f"Calendar tool: Retrieved real schedule for user {user_id}")
            return schedule_data
            
        except Exception as e:
            logger.error(f"Calendar tool error: {e}")
            return CalendarTool._get_fallback_schedule(date)
    
    @staticmethod
    def _get_fallback_schedule(date: str) -> Dict[str, Any]:
        """Fallback schedule when Google Calendar is unavailable."""
        return {
            "date": date,
            "meetings": 0,
            "total_hours": 0,
            "stress_level": "unknown",
            "description": "Unable to retrieve schedule",
            "events": []
        }

class HealthTrackingTool:
    """Google Fit API for health tracking."""
    
    @staticmethod
    def get_health_data(user_id: int, access_token: str = None) -> Dict[str, Any]:
        """
        Get user's Google Fit health tracking data.
        
        Args:
            user_id: User ID
            access_token: Google OAuth access token
        
        Returns:
            Dict with health metrics
        """
        try:
            if not access_token:
                logger.warning("No access token provided for Google Fit")
                return HealthTrackingTool._get_fallback_health_data()
            
            # Create credentials from access token
            credentials = Credentials(
                token=access_token,
                client_id=GOOGLE_CLIENT_ID,
                client_secret=GOOGLE_CLIENT_SECRET,
                token_uri="https://oauth2.googleapis.com/token"
            )
            
            # Build Fitness service
            service = build('fitness', 'v1', credentials=credentials)
            
            # Get today's date range
            end_time = datetime.now()
            start_time = end_time.replace(hour=0, minute=0, second=0, microsecond=0)
            
            # Convert to nanoseconds (Google Fit requirement)
            start_ns = int(start_time.timestamp() * 1000000000)
            end_ns = int(end_time.timestamp() * 1000000000)
            
            health_data = {
                "hydration": HealthTrackingTool._get_hydration_data(service, start_ns, end_ns),
                "exercise": HealthTrackingTool._get_exercise_data(service, start_ns, end_ns),
                "sleep": HealthTrackingTool._get_sleep_data(service, start_ns, end_ns),
                "nutrition": HealthTrackingTool._get_nutrition_data(service, start_ns, end_ns),
                "stress": HealthTrackingTool._get_stress_data(service, start_ns, end_ns)
            }
            
            logger.info(f"Health tracking tool: Retrieved real data for user {user_id}")
            return health_data
            
        except Exception as e:
            logger.error(f"Health tracking tool error: {e}")
            return HealthTrackingTool._get_fallback_health_data()
    
    @staticmethod
    def _get_hydration_data(service, start_ns: int, end_ns: int) -> Dict[str, Any]:
        """Get hydration data from Google Fit."""
        try:
            # Google Fit doesn't have direct hydration tracking, so we'll use water intake
            # This would need to be implemented with a custom data source or app integration
            return {
                "water_intake_ml": 0,
                "daily_goal_ml": 2000,
                "percentage": 0,
                "status": "unknown",
                "last_drink": None
            }
        except Exception as e:
            logger.error(f"Hydration data error: {e}")
            return {"status": "unknown"}
    
    @staticmethod
    def _get_exercise_data(service, start_ns: int, end_ns: int) -> Dict[str, Any]:
        """Get exercise data from Google Fit."""
        try:
            # Get step count
            steps_data = service.users().dataSources().datasets().get(
                userId='me',
                dataSourceId='derived:com.google.step_count.delta:com.google.android.gms:estimated_steps',
                datasetId=f"{start_ns}-{end_ns}"
            ).execute()
            
            steps_today = 0
            if 'point' in steps_data:
                for point in steps_data['point']:
                    if 'value' in point:
                        steps_today += point['value'][0].get('intVal', 0)
            
            # Get activity data
            activity_data = service.users().sessions().list(
                userId='me',
                startTime=f"{start_ns}ns",
                endTime=f"{end_ns}ns",
                activityType=8  # 8 = workout
            ).execute()
            
            workout_minutes = 0
            workout_type = "none"
            
            if 'session' in activity_data:
                for session in activity_data['session']:
                    start_time = int(session['startTimeMillis']) / 1000000000
                    end_time = int(session['endTimeMillis']) / 1000000000
                    duration = (end_time - start_time) / 60  # Convert to minutes
                    workout_minutes += duration
                    workout_type = session.get('activityType', 'workout')
            
            # Calculate status
            steps_pct = (steps_today / 10000) * 100
            if steps_pct >= 100 and workout_minutes >= 30:
                status = "excellent"
            elif steps_pct >= 70 or workout_minutes >= 20:
                status = "good"
            elif steps_pct >= 50:
                status = "moderate"
            else:
                status = "needs_improvement"
            
            return {
                "steps_today": steps_today,
                "daily_goal": 10000,
                "workout_minutes": int(workout_minutes),
                "workout_type": workout_type,
                "status": status
            }
            
        except Exception as e:
            logger.error(f"Exercise data error: {e}")
            return {"status": "unknown"}
    
    @staticmethod
    def _get_sleep_data(service, start_ns: int, end_ns: int) -> Dict[str, Any]:
        """Get sleep data from Google Fit."""
        try:
            # Get sleep sessions
            sleep_data = service.users().sessions().list(
                userId='me',
                startTime=f"{start_ns}ns",
                endTime=f"{end_ns}ns",
                activityType=72  # 72 = sleep
            ).execute()
            
            hours_last_night = 0
            quality_score = 5  # Default score
            
            if 'session' in sleep_data:
                for session in sleep_data['session']:
                    start_time = int(session['startTimeMillis']) / 1000000000
                    end_time = int(session['endTimeMillis']) / 1000000000
                    duration = (end_time - start_time) / 3600  # Convert to hours
                    hours_last_night += duration
                    
                    # Estimate quality based on duration
                    if duration >= 7 and duration <= 9:
                        quality_score = 8
                    elif duration >= 6 and duration <= 10:
                        quality_score = 6
                    else:
                        quality_score = 4
            
            # Calculate status
            if hours_last_night >= 7 and quality_score >= 7:
                status = "excellent"
            elif hours_last_night >= 6 and quality_score >= 5:
                status = "good"
            elif hours_last_night >= 5:
                status = "moderate"
            else:
                status = "poor"
            
            return {
                "hours_last_night": round(hours_last_night, 1),
                "quality_score": quality_score,
                "recommended_hours": 8,
                "bedtime": None,  # Would need additional processing
                "wake_time": None,  # Would need additional processing
                "status": status
            }
            
        except Exception as e:
            logger.error(f"Sleep data error: {e}")
            return {"status": "unknown"}
    
    @staticmethod
    def _get_nutrition_data(service, start_ns: int, end_ns: int) -> Dict[str, Any]:
        """Get nutrition data from Google Fit."""
        try:
            # Google Fit has limited nutrition tracking
            # This would typically require integration with nutrition apps
            return {
                "meals_logged": 0,
                "vitamins_taken": False,
                "caffeine_intake": 0,
                "alcohol_intake": 0,
                "status": "unknown"
            }
        except Exception as e:
            logger.error(f"Nutrition data error: {e}")
            return {"status": "unknown"}
    
    @staticmethod
    def _get_stress_data(service, start_ns: int, end_ns: int) -> Dict[str, Any]:
        """Get stress data from Google Fit."""
        try:
            # Google Fit doesn't have direct stress tracking
            # This would require integration with stress monitoring apps or devices
            return {
                "stress_level": 5,  # Default moderate level
                "meditation_minutes": 0,
                "breathing_exercises": 0,
                "status": "moderate"
            }
        except Exception as e:
            logger.error(f"Stress data error: {e}")
            return {"status": "unknown"}
    
    @staticmethod
    def _get_fallback_health_data() -> Dict[str, Any]:
        """Fallback health data when Google Fit is unavailable."""
        return {
            "hydration": {"status": "unknown", "percentage": 0},
            "exercise": {"status": "unknown"},
            "sleep": {"status": "unknown"},
            "nutrition": {"status": "unknown"},
            "stress": {"status": "unknown"}
        }

class MedicalInfoTool:
    """Medical information APIs for evidence-based advice."""
    
    @staticmethod
    def get_medical_info(symptom: str, cycle_phase: str = None) -> Dict[str, Any]:
        """
        Get evidence-based medical information.
        
        Args:
            symptom: Symptom to research
            cycle_phase: Current cycle phase (optional)
        
        Returns:
            Dict with medical information
        """
        try:
            # Mock medical database - in production, this would call medical APIs
            medical_database = {
                "cramps": {
                    "description": "Menstrual cramps are caused by uterine contractions",
                    "normal_phase": "menstrual",
                    "remedies": [
                        "Heat therapy (heating pad)",
                        "Over-the-counter pain relievers (ibuprofen)",
                        "Gentle exercise and stretching",
                        "Adequate hydration"
                    ],
                    "when_to_see_doctor": "If cramps are severe or accompanied by heavy bleeding",
                    "evidence_level": "high"
                },
                "fatigue": {
                    "description": "Fatigue during menstruation is common due to hormonal changes",
                    "normal_phase": "menstrual",
                    "remedies": [
                        "Ensure adequate sleep (7-9 hours)",
                        "Gentle exercise to boost energy",
                        "Iron-rich foods if experiencing heavy bleeding",
                        "Stay hydrated"
                    ],
                    "when_to_see_doctor": "If fatigue is severe or persistent",
                    "evidence_level": "high"
                },
                "mood_changes": {
                    "description": "Hormonal fluctuations can cause mood changes throughout the cycle",
                    "normal_phase": "luteal",
                    "remedies": [
                        "Regular exercise",
                        "Stress management techniques",
                        "Adequate sleep",
                        "Support from partner/friends"
                    ],
                    "when_to_see_doctor": "If mood changes are severe or affect daily life",
                    "evidence_level": "high"
                },
                "bloating": {
                    "description": "Water retention and hormonal changes can cause bloating",
                    "normal_phase": "luteal",
                    "remedies": [
                        "Reduce salt intake",
                        "Stay hydrated",
                        "Gentle exercise",
                        "Avoid carbonated beverages"
                    ],
                    "when_to_see_doctor": "If bloating is severe or persistent",
                    "evidence_level": "medium"
                }
            }
            
            # Get medical info for the symptom
            if symptom.lower() in medical_database:
                info = medical_database[symptom.lower()].copy()
                
                # Add phase-specific information if available
                if cycle_phase and info.get("normal_phase") == cycle_phase:
                    info["phase_relevant"] = True
                    info["phase_note"] = f"This symptom is common during the {cycle_phase} phase"
                else:
                    info["phase_relevant"] = False
                
                logger.info(f"Medical info tool: Retrieved info for symptom '{symptom}'")
                return info
            else:
                return {
                    "description": "Symptom not found in medical database",
                    "remedies": ["Consult with healthcare provider"],
                    "evidence_level": "unknown"
                }
                
        except Exception as e:
            logger.error(f"Medical info tool error: {e}")
            return {
                "description": "Unable to retrieve medical information",
                "remedies": ["Consult with healthcare provider"],
                "evidence_level": "unknown"
            } 