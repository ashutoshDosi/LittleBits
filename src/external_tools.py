"""
external_tools.py

External tool integrations for CycleWise agentic AI:
- Calendar API for stress correlation
- Health tracking APIs (hydration, exercise, sleep)
- Medical information APIs for evidence-based advice

Note: For hackathon demo, using mock implementations.
In production, these would connect to real APIs.
"""

import requests
import logging
from typing import Dict, Any, Optional
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

# Mock API configurations (replace with real APIs in production)
WEATHER_API_KEY = "mock_weather_key"
CALENDAR_API_KEY = "mock_calendar_key"
HEALTH_API_KEY = "mock_health_key"

class CalendarTool:
    """Calendar integration for stress correlation."""
    
    @staticmethod
    def get_user_schedule(user_id: int, date: str = None) -> Dict[str, Any]:
        """
        Get user's calendar schedule for stress correlation.
        
        Args:
            user_id: User ID
            date: Date to check (default: today)
        
        Returns:
            Dict with schedule information
        """
        try:
            # Mock implementation - in production, this would call Google Calendar API
            if date is None:
                date = datetime.now().strftime("%Y-%m-%d")
            
            # Simulate different stress levels based on schedule
            mock_schedules = {
                "high_stress": {
                    "date": date,
                    "meetings": 5,
                    "total_hours": 10,
                    "stress_level": "high",
                    "description": "Heavy meeting day with 5 meetings and 10 hours of work"
                },
                "medium_stress": {
                    "date": date,
                    "meetings": 3,
                    "total_hours": 8,
                    "stress_level": "medium", 
                    "description": "Moderate day with 3 meetings and 8 hours of work"
                },
                "low_stress": {
                    "date": date,
                    "meetings": 1,
                    "total_hours": 6,
                    "stress_level": "low",
                    "description": "Light day with 1 meeting and 6 hours of work"
                }
            }
            
            # Simulate different stress levels based on user_id
            stress_levels = ["high_stress", "medium_stress", "low_stress"]
            selected_level = stress_levels[user_id % 3]
            
            logger.info(f"Calendar tool: Retrieved schedule for user {user_id}")
            return mock_schedules[selected_level]
            
        except Exception as e:
            logger.error(f"Calendar tool error: {e}")
            return {
                "date": date,
                "meetings": 0,
                "total_hours": 0,
                "stress_level": "unknown",
                "description": "Unable to retrieve schedule"
            }

class HealthTrackingTool:
    """Health tracking APIs for hydration, exercise, sleep."""
    
    @staticmethod
    def get_health_data(user_id: int) -> Dict[str, Any]:
        """
        Get user's health tracking data.
        
        Args:
            user_id: User ID
        
        Returns:
            Dict with health metrics
        """
        try:
            # Mock implementation - in production, this would call health tracking APIs
            mock_health_data = {
                "hydration": {
                    "water_intake_ml": 1200,
                    "daily_goal_ml": 2000,
                    "percentage": 60,
                    "status": "needs_improvement"
                },
                "exercise": {
                    "steps_today": 6500,
                    "daily_goal": 10000,
                    "workout_minutes": 30,
                    "status": "moderate"
                },
                "sleep": {
                    "hours_last_night": 7.5,
                    "quality_score": 8,
                    "recommended_hours": 8,
                    "status": "good"
                },
                "nutrition": {
                    "meals_logged": 2,
                    "vitamins_taken": True,
                    "status": "partial"
                }
            }
            
            # Vary data based on user_id for demo
            if user_id % 3 == 0:
                mock_health_data["hydration"]["water_intake_ml"] = 1800
                mock_health_data["hydration"]["percentage"] = 90
                mock_health_data["hydration"]["status"] = "good"
            
            logger.info(f"Health tracking tool: Retrieved data for user {user_id}")
            return mock_health_data
            
        except Exception as e:
            logger.error(f"Health tracking tool error: {e}")
            return {
                "hydration": {"status": "unknown"},
                "exercise": {"status": "unknown"},
                "sleep": {"status": "unknown"},
                "nutrition": {"status": "unknown"}
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

class WeatherTool:
    """Weather API for symptom correlation."""
    
    @staticmethod
    def get_weather_data(location: str = "default") -> Dict[str, Any]:
        """
        Get weather data for symptom correlation.
        
        Args:
            location: Location to check weather
        
        Returns:
            Dict with weather information
        """
        try:
            # Mock weather data - in production, this would call OpenWeatherMap API
            mock_weather = {
                "temperature": 72,
                "condition": "sunny",
                "humidity": 45,
                "pressure": 1013,
                "description": "Sunny and mild weather",
                "impact_on_symptoms": "Good weather may improve energy levels and mood"
            }
            
            # Vary weather based on location for demo
            if "rain" in location.lower():
                mock_weather.update({
                    "condition": "rainy",
                    "temperature": 65,
                    "description": "Rainy and cool weather",
                    "impact_on_symptoms": "Rainy weather may affect mood and energy levels"
                })
            
            logger.info(f"Weather tool: Retrieved weather data for {location}")
            return mock_weather
            
        except Exception as e:
            logger.error(f"Weather tool error: {e}")
            return {
                "temperature": 70,
                "condition": "unknown",
                "description": "Weather data unavailable",
                "impact_on_symptoms": "Unable to determine weather impact"
            } 