"""
external_tools.py

External integrations for CycleWise:
- Google Calendar API for daily meeting counts and total meeting hours
- Google Fit API for sleep tracking (past 24 hours)

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


class HealthTrackingTool:
    """Google Fit integration for sleep tracking only."""

    @staticmethod
    def get_health_data(user_id: int, access_token: str) -> Dict[str, Any]:
        """
        Get user's sleep duration from Google Fit over past 24 hours.
        Args:
            user_id (int): ID of the user
            access_token (str): OAuth 2.0 access token
        Returns:
            Dict[str, Any]: { sleep: { hours_last_night: float, status: str } }
        """
        try:
            creds = Credentials(token=access_token)
            fitness = build('fitness', 'v1', credentials=creds)

            end_time_millis = int(datetime.utcnow().timestamp() * 1000)
            start_time_millis = int((datetime.utcnow() - timedelta(days=1)).timestamp() * 1000)
            dataset_id = f"{start_time_millis}-{end_time_millis}"

            # Get available data sources
            data_sources = fitness.users().dataSources().list(userId='me').execute()
            sleep_source_id = None

            for source in data_sources.get("dataSource", []):
                if "com.google.sleep.segment" in source.get("dataType", {}).get("name", ""):
                    sleep_source_id = source["dataStreamId"]
                    break

            if not sleep_source_id:
                raise ValueError("No sleep data source found.")

            dataset = fitness.users().dataSources().datasets().get(
                userId='me',
                dataSourceId=sleep_source_id,
                datasetId=dataset_id
            ).execute()

            total_sleep_ms = 0
            for point in dataset.get("point", []):
                sleep_stage = point.get("value", [{}])[0].get("intVal", -1)
                if sleep_stage in [1, 2, 3, 4, 5]:  # All sleep stages
                    start = int(point["startTimeNanos"]) // 1_000_000
                    end = int(point["endTimeNanos"]) // 1_000_000
                    total_sleep_ms += (end - start)

            sleep_hours = round(total_sleep_ms / (1000 * 60 * 60), 2)

            return {
                "sleep": {
                    "hours_last_night": sleep_hours,
                    "status": HealthTrackingTool.evaluate_sleep_status(sleep_hours)
                }
            }

        except Exception as e:
            logger.error(f"Sleep tracking error: {e}")
            return {
                "sleep": {
                    "hours_last_night": 0.0,
                    "status": "unknown"
                }
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
