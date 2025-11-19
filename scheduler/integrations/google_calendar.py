"""
Mock Google Calendar integration for Sprint 3.

This module provides placeholder functions for Google Calendar integration.
In future sprints, these will be replaced with actual Google Calendar API calls.
"""
from datetime import datetime, timedelta
import random
from typing import List, Dict, Optional, Tuple


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


# Convenience functions for easy import
def get_free_busy_for_user(user, start_time, end_time):
    """Wrapper for MockGoogleCalendar.get_free_busy_for_user"""
    return MockGoogleCalendar.get_free_busy_for_user(user, start_time, end_time)


def find_common_free_slots(users, time_options):
    """Wrapper for MockGoogleCalendar.find_common_free_slots"""
    return MockGoogleCalendar.find_common_free_slots(users, time_options)


def create_calendar_event(user, title, start_time, end_time, attendees=None, description=""):
    """Wrapper for MockGoogleCalendar.create_calendar_event"""
    return MockGoogleCalendar.create_calendar_event(
        user, title, start_time, end_time, attendees, description
    )
