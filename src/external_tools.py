"""
external_tools.py

External integrations for CycleWise:
- Google Calendar API for daily meeting counts and total meeting hours
- Google Fit API for sleep tracking (past 24 hours)
- Medical information database for symptom research
- Weather API for symptom correlation

NOTE: Requires valid OAuth 2.0 access tokens per user session.
"""

import logging
from typing import Dict, Any
from datetime import datetime, timedelta
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CalendarTool:
    """Google Calendar tool to fetch meeting data."""

    @staticmethod
    def get_calendar_data(access_token: str) -> Dict[str, Any]:
        """
        Fetch number of meetings and total meeting duration today.
        Args:
            access_token (str): OAuth 2.0 access token
        Returns:
            Dict[str, Any]: { meeting_count: int, total_hours: float }
        """
        try:
            creds = Credentials(token=access_token)
            service = build('calendar', 'v3', credentials=creds)

            now = datetime.utcnow()
            start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0).isoformat() + 'Z'
            end_of_day = now.replace(hour=23, minute=59, second=59).isoformat() + 'Z'

            events_result = service.events().list(
                calendarId='primary',
                timeMin=start_of_day,
                timeMax=end_of_day,
                singleEvents=True,
                orderBy='startTime'
            ).execute()

            events = events_result.get('items', [])
            total_minutes = 0

            for event in events:
                start = event.get('start', {}).get('dateTime')
                end = event.get('end', {}).get('dateTime')
                if start and end:
                    start_dt = datetime.fromisoformat(start)
                    end_dt = datetime.fromisoformat(end)
                    duration = (end_dt - start_dt).total_seconds() / 60
                    total_minutes += duration

            meeting_count = len(events)
            total_hours = round(total_minutes / 60, 2)

            return {
                "meeting_count": meeting_count,
                "total_hours": total_hours
            }

        except Exception as e:
            logger.error(f"Calendar API error: {e}")
            return {
                "meeting_count": 0,
                "total_hours": 0.0
            }

    @staticmethod
    def get_user_schedule(user_id: int) -> Dict[str, Any]:
        """
        Get user's schedule and stress level for correlation with symptoms.
        Args:
            user_id (int): The user's ID
        Returns:
            Dict[str, Any]: Schedule and stress information
        """
        try:
            # Mock implementation - in production, this would use real calendar data
            return {
                "description": "3 meetings today, 2 hours total",
                "stress_level": "moderate",
                "meeting_count": 3,
                "total_hours": 2.0,
                "next_meeting": "2:00 PM",
                "free_time": "1:00 PM - 2:00 PM"
            }
        except Exception as e:
            logger.error(f"Schedule retrieval error: {e}")
            return {
                "description": "No schedule data available",
                "stress_level": "unknown",
                "meeting_count": 0,
                "total_hours": 0.0
            }


class HealthTrackingTool:
    """Google Fit integration for sleep tracking only."""

    @staticmethod
    def get_sleep_data(user_id: int):
        # TODO: Integrate with Google Fit or use mock data for now
        return {
            "hours_last_night": 7.5,
            "quality_score": 8,
            "recommended_hours": 8,
            "status": "good"
        }

    @staticmethod
    def get_health_data(user_id: int, access_token: str = None) -> Dict[str, Any]:
        """
        Get user's health data including hydration, exercise, and sleep.
        Args:
            user_id (int): ID of the user
            access_token (str): OAuth 2.0 access token (optional for mock data)
        Returns:
            Dict[str, Any]: Health data including hydration, exercise, and sleep
        """
        try:
            # Mock implementation - in production, this would use Google Fit API
            return {
                "hydration": {
                    "percentage": 75,
                    "water_intake_ml": 1500,
                    "recommended_ml": 2000,
                    "status": "needs_improvement"
                },
                "exercise": {
                    "steps_today": 6500,
                    "calories_burned": 320,
                    "active_minutes": 45,
                    "status": "moderate"
                },
                "sleep": {
                    "hours_last_night": 7.5,
                    "quality_score": 8,
                    "recommended_hours": 8,
                    "status": "good"
                }
            }
        except Exception as e:
            logger.error(f"Health data retrieval error: {e}")
            return {
                "hydration": {"percentage": 0, "water_intake_ml": 0, "status": "unknown"},
                "exercise": {"steps_today": 0, "status": "unknown"},
                "sleep": {"hours_last_night": 0, "status": "unknown"}
            }

    @staticmethod
    def evaluate_sleep_status(hours: float) -> str:
        if hours >= 7.5:
            return "good"
        elif 6 <= hours < 7.5:
            return "moderate"
        elif 0 < hours < 6:
            return "needs_improvement"
        return "unknown"


class MedicalInfoTool:
    """Medical information database for symptom research and remedies."""

    @staticmethod
    def get_medical_info(symptom: str = None, phase: str = None) -> Dict[str, Any]:
        """
        Get evidence-based medical information for symptoms.
        Args:
            symptom (str): The symptom to research
            phase (str): The menstrual phase (optional)
        Returns:
            Dict[str, Any]: Medical information and remedies
        """
        # Medical database for common menstrual symptoms
        medical_database = {
            "cramps": {
                "description": "Menstrual cramps (dysmenorrhea) are caused by uterine contractions.",
                "evidence_level": "high",
                "remedies": [
                    "Heat therapy (heating pad, warm bath)",
                    "Over-the-counter pain relievers (ibuprofen, naproxen)",
                    "Gentle exercise and stretching",
                    "Magnesium supplements",
                    "Acupuncture or acupressure"
                ],
                "when_to_see_doctor": "Severe pain, pain that doesn't improve with treatment, or pain that interferes with daily activities"
            },
            "fatigue": {
                "description": "Fatigue during menstruation is common due to hormonal changes and blood loss.",
                "evidence_level": "high",
                "remedies": [
                    "Prioritize sleep and rest",
                    "Stay hydrated",
                    "Eat iron-rich foods",
                    "Gentle exercise",
                    "Avoid caffeine and alcohol"
                ],
                "when_to_see_doctor": "Extreme fatigue, fatigue that doesn't improve, or fatigue with other concerning symptoms"
            },
            "mood_changes": {
                "description": "Hormonal fluctuations can cause mood swings, irritability, and emotional sensitivity.",
                "evidence_level": "high",
                "remedies": [
                    "Practice stress management techniques",
                    "Regular exercise",
                    "Adequate sleep",
                    "Mindfulness and meditation",
                    "Talk to a trusted friend or therapist"
                ],
                "when_to_see_doctor": "Severe mood changes, thoughts of self-harm, or mood changes that significantly impact daily life"
            },
            "bloating": {
                "description": "Water retention and hormonal changes can cause bloating during the menstrual cycle.",
                "evidence_level": "moderate",
                "remedies": [
                    "Reduce salt intake",
                    "Stay hydrated",
                    "Gentle exercise",
                    "Avoid carbonated beverages",
                    "Eat smaller, more frequent meals"
                ],
                "when_to_see_doctor": "Severe bloating, bloating with other concerning symptoms, or bloating that doesn't improve"
            },
            "headaches": {
                "description": "Hormonal changes can trigger headaches, especially during the luteal phase.",
                "evidence_level": "high",
                "remedies": [
                    "Stay hydrated",
                    "Get adequate sleep",
                    "Manage stress",
                    "Over-the-counter pain relievers",
                    "Avoid trigger foods (chocolate, caffeine, alcohol)"
                ],
                "when_to_see_doctor": "Severe headaches, headaches with visual changes, or headaches that don't respond to treatment"
            }
        }

        if symptom and symptom.lower() in medical_database:
            return medical_database[symptom.lower()]
        elif symptom:
            # Return general information for unknown symptoms
            return {
                "description": f"Information about {symptom} during menstruation",
                "evidence_level": "low",
                "remedies": [
                    "Consult with a healthcare provider",
                    "Track symptoms in a journal",
                    "Practice general self-care"
                ],
                "when_to_see_doctor": "If symptoms are severe, persistent, or concerning"
            }
        else:
            # Return general menstrual health information
            return {
                "description": "General menstrual health information and self-care tips",
                "evidence_level": "high",
                "remedies": [
                    "Maintain a healthy diet",
                    "Exercise regularly",
                    "Get adequate sleep",
                    "Manage stress",
                    "Track your cycle"
                ],
                "when_to_see_doctor": "For irregular cycles, severe symptoms, or any concerning changes"
            }


class WeatherTool:
    """Weather API integration for symptom correlation."""

    @staticmethod
    def get_weather_data() -> Dict[str, Any]:
        """
        Get current weather data for symptom correlation.
        Returns:
            Dict[str, Any]: Weather information and potential impact on symptoms
        """
        try:
            # Mock implementation - in production, this would use a weather API
            return {
                "temperature": 72,
                "description": "Partly cloudy",
                "humidity": 65,
                "pressure": 1013,
                "impact_on_symptoms": "Moderate humidity may affect bloating and discomfort. Consider staying hydrated and avoiding salty foods."
            }
        except Exception as e:
            logger.error(f"Weather data retrieval error: {e}")
            return {
                "temperature": 70,
                "description": "Unknown",
                "humidity": 50,
                "pressure": 1013,
                "impact_on_symptoms": "Weather data unavailable. Focus on general self-care practices."
            }
