"""
Google Calendar integration.

Uses real Google Calendar API when a user has connected their Google account.
Falls back to mock behavior if credentials are missing or any API error occurs.
"""
from datetime import datetime, timedelta
import random
from typing import List, Dict, Optional, Tuple

from django.conf import settings
from django.utils import timezone as dj_timezone

from scheduler.models import GoogleOAuthCredential

# Keep the existing mock for fallback
class MockGoogleCalendar:
    """Mock implementation of Google Calendar integration."""
    
    @staticmethod
    def get_free_busy_for_user(user, start_time: datetime, end_time: datetime) -> List[Dict]:
        """
        Get free/busy information for a user within a time range.
        
        Args:
            user: Django User object
            start_time: Start of the time range
            end_time: End of the time range
            
        Returns:
            List of busy time slots (mocked data)
        """
        # For Sprint 3, return some mock busy periods
        busy_slots = []
        
        # Simulate some random busy slots
        current = start_time
        while current < end_time:
            # 30% chance of being busy at any given hour
            if random.random() < 0.3:
                busy_start = current
                busy_end = current + timedelta(hours=random.choice([1, 2]))
                if busy_end <= end_time:
                    busy_slots.append({
                        'start': busy_start,
                        'end': busy_end,
                        'status': 'busy'
                    })
            current += timedelta(hours=1)
        
        return busy_slots
    
    @staticmethod
    def find_common_free_slots(users: List, time_options: List[Tuple[datetime, datetime]]) -> List[Dict]:
        """
        Find common free time slots among multiple users.
        
        Args:
            users: List of Django User objects
            time_options: List of (start_time, end_time) tuples to check
            
        Returns:
            List of available time slots with availability info
        """
        results = []
        
        for start_time, end_time in time_options:
            # For Sprint 3, randomly determine if slot is available
            # In reality, this would check each user's calendar
            availability_score = random.uniform(0.5, 1.0)  # 50-100% availability
            
            results.append({
                'start_time': start_time,
                'end_time': end_time,
                'available': availability_score > 0.7,  # Consider >70% as available
                'availability_score': availability_score,
                'conflicts': [] if availability_score > 0.7 else ['Mock conflict with existing event']
            })
        
        return results
    
    @staticmethod
    def create_calendar_event(user, title: str, start_time: datetime, end_time: datetime, 
                            attendees: Optional[List] = None, description: str = "") -> Dict:
        """
        Create a calendar event (mocked).
        
        Args:
            user: Organizer User object
            title: Event title
            start_time: Event start time
            end_time: Event end time
            attendees: List of attendee email addresses
            description: Event description
            
        Returns:
            Mock event creation response
        """
        return {
            'status': 'success',
            'event_id': f'mock_event_{random.randint(1000, 9999)}',
            'message': 'Event would be created in Google Calendar',
            'details': {
                'title': title,
                'start': start_time.isoformat(),
                'end': end_time.isoformat(),
                'organizer': user.email,
                'attendees': attendees or [],
                'description': description
            }
        }
    
    @staticmethod
    def check_availability_message(meeting_request) -> str:
        """
        Generate a mock availability check message for display.
        
        Args:
            meeting_request: MeetingRequest object
            
        Returns:
            String message about availability
        """
        if meeting_request.has_selected_time:
            selected = meeting_request.selected_time
            # Simulate checking availability
            if random.random() > 0.3:
                return f"✅ All participants appear to be free from {selected.start_time.strftime('%H:%M')} to {selected.end_time.strftime('%H:%M')} on {selected.start_time.strftime('%Y-%m-%d')}"
            else:
                return f"⚠️ Some participants may have conflicts from {selected.start_time.strftime('%H:%M')} to {selected.end_time.strftime('%H:%M')} on {selected.start_time.strftime('%Y-%m-%d')}"
        return "No time selected yet"


# Try to import Google API libs (installed via requirements)
try:
    from googleapiclient.discovery import build
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request
    GOOGLE_LIBS_AVAILABLE = True
except Exception:
    GOOGLE_LIBS_AVAILABLE = False


def _get_user_credentials(user):
    """Build google.oauth2.credentials.Credentials from stored DB record."""
    if not GOOGLE_LIBS_AVAILABLE:
        return None
    try:
        cred = GoogleOAuthCredential.objects.get(user=user)
    except GoogleOAuthCredential.DoesNotExist:
        return None

    scopes = (cred.scopes or '').split() if cred.scopes else settings.GOOGLE_OAUTH_SCOPES
    creds = Credentials(
        token=cred.token,
        refresh_token=cred.refresh_token,
        token_uri=cred.token_uri or 'https://oauth2.googleapis.com/token',
        client_id=settings.GOOGLE_OAUTH_CLIENT_ID,
        client_secret=settings.GOOGLE_OAUTH_CLIENT_SECRET,
        scopes=scopes,
    )
    # Refresh if needed
    try:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            # Persist updated tokens
            cred.token = creds.token
            # refresh_token might be None on refresh; keep existing if not returned
            if getattr(creds, 'refresh_token', None):
                cred.refresh_token = creds.refresh_token
            cred.expiry = getattr(creds, 'expiry', None)
            cred.scopes = ' '.join(scopes)
            cred.save(update_fields=['token', 'refresh_token', 'expiry', 'scopes', 'updated_at'])
    except Exception:
        return None

    return creds


def _build_calendar_service(user):
    """Create Calendar API service for a connected user."""
    creds = _get_user_credentials(user)
    if not creds:
        return None
    try:
        # cache_discovery=False avoids write access in read-only environments
        return build('calendar', 'v3', credentials=creds, cache_discovery=False)
    except Exception:
        return None


def _real_get_free_busy_for_user(user, start_time: datetime, end_time: datetime) -> List[Dict]:
    """Real API: free/busy for the user's primary calendar."""
    service = _build_calendar_service(user)
    if not service:
        return MockGoogleCalendar.get_free_busy_for_user(user, start_time, end_time)

    body = {
        "timeMin": start_time.astimezone(dj_timezone.utc).isoformat().replace('+00:00', 'Z'),
        "timeMax": end_time.astimezone(dj_timezone.utc).isoformat().replace('+00:00', 'Z'),
        "items": [{"id": "primary"}],
    }
    try:
        resp = service.freebusy().query(body=body).execute()
        busy = resp.get('calendars', {}).get('primary', {}).get('busy', [])
        # Normalize to our structure
        return [{'start': b['start'], 'end': b['end'], 'status': 'busy'} for b in busy]
    except Exception:
        return MockGoogleCalendar.get_free_busy_for_user(user, start_time, end_time)


def _real_create_calendar_event(user, title: str, start_time: datetime, end_time: datetime,
                                attendees: Optional[List] = None, description: str = "") -> Dict:
    """Real API: create an event on the user's primary calendar."""
    service = _build_calendar_service(user)
    if not service:
        return MockGoogleCalendar.create_calendar_event(user, title, start_time, end_time, attendees, description)

    event = {
        'summary': title,
        'description': description,
        'start': {
            'dateTime': start_time.astimezone(dj_timezone.utc).isoformat().replace('+00:00', 'Z'),
            'timeZone': 'UTC',
        },
        'end': {
            'dateTime': end_time.astimezone(dj_timezone.utc).isoformat().replace('+00:00', 'Z'),
            'timeZone': 'UTC',
        },
        'attendees': [{'email': a} for a in (attendees or [])],
    }
    try:
        created = service.events().insert(calendarId='primary', body=event, sendUpdates='all').execute()
        return {
            'status': 'success',
            'event_id': created.get('id', f'google_event_{random.randint(1000, 9999)}'),
            'message': 'Event created in Google Calendar',
            'details': {
                'title': title,
                'start': event['start']['dateTime'],
                'end': event['end']['dateTime'],
                'organizer': user.email,
                'attendees': attendees or [],
                'description': description
            }
        }
    except Exception:
        return MockGoogleCalendar.create_calendar_event(user, title, start_time, end_time, attendees, description)


def _real_check_availability_message(meeting_request) -> str:
    """Real API: human message based on free/busy for selected time, else fallback."""
    if not meeting_request.has_selected_time:
        return "No time selected yet"
    selected = meeting_request.selected_time
    service = _build_calendar_service(meeting_request.organizer)
    if not service:
        return MockGoogleCalendar.check_availability_message(meeting_request)

    body = {
        "timeMin": selected.start_time.astimezone(dj_timezone.utc).isoformat().replace('+00:00', 'Z'),
        "timeMax": selected.end_time.astimezone(dj_timezone.utc).isoformat().replace('+00:00', 'Z'),
        "items": [{"id": "primary"}],
    }
    try:
        resp = service.freebusy().query(body=body).execute()
        busy = resp.get('calendars', {}).get('primary', {}).get('busy', [])
        if not busy:
            return f"✅ Your primary calendar appears free from {selected.start_time.strftime('%H:%M')} to {selected.end_time.strftime('%H:%M')} on {selected.start_time.strftime('%Y-%m-%d')}"
        return f"⚠️ You have conflicts during {selected.start_time.strftime('%H:%M')}–{selected.end_time.strftime('%H:%M')} on {selected.start_time.strftime('%Y-%m-%d')}"
    except Exception:
        return MockGoogleCalendar.check_availability_message(meeting_request)


# Public helpers (keep names so existing imports continue to work)
def get_free_busy_for_user(user, start_time, end_time):
    """Return real free/busy if connected, else mock."""
    return _real_get_free_busy_for_user(user, start_time, end_time)


def find_common_free_slots(users, time_options):
    """Simple heuristic; real multi-user check is out of scope here."""
    # Preserve existing mocked behavior for Sprint 3 scope
    results = []
    for start_time, end_time in time_options:
        availability_score = random.uniform(0.5, 1.0)
        results.append({
            'start_time': start_time,
            'end_time': end_time,
            'available': availability_score > 0.7,
            'availability_score': availability_score,
            'conflicts': [] if availability_score > 0.7 else ['Mock conflict with existing event']
        })
    return results


def create_calendar_event(user, title, start_time, end_time, attendees=None, description=""):
    """Create event in real calendar if connected; otherwise fallback to mock."""
    return _real_create_calendar_event(user, title, start_time, end_time, attendees, description)


# Convenience method used by MeetingDetailView
def check_availability_message(meeting_request) -> str:
    return _real_check_availability_message(meeting_request)
