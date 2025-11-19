from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from .models import MeetingRequest, TimeOption
from .integrations.google_calendar import MockGoogleCalendar, get_free_busy_for_user, create_calendar_event


class GoogleCalendarIntegrationTest(TestCase):
    """Test the mocked Google Calendar integration."""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com'
        )
        self.meeting = MeetingRequest.objects.create(
            organizer=self.user,
            title='Test Meeting'
        )
    
    def test_get_free_busy_returns_data(self):
        """Test that free/busy mock returns some data."""
        start = timezone.now()
        end = start + timedelta(hours=8)
        
        busy_slots = get_free_busy_for_user(self.user, start, end)
        
        # Should return a list
        self.assertIsInstance(busy_slots, list)
        
        # If there are busy slots, they should have the right structure
        for slot in busy_slots:
            self.assertIn('start', slot)
            self.assertIn('end', slot)
            self.assertIn('status', slot)
            self.assertEqual(slot['status'], 'busy')
    
    def test_create_calendar_event_mock(self):
        """Test the mock calendar event creation."""
        start = timezone.now() + timedelta(days=1)
        end = start + timedelta(hours=1)
        
        response = create_calendar_event(
            user=self.user,
            title='Test Event',
            start_time=start,
            end_time=end,
            attendees=['attendee@example.com'],
            description='Test description'
        )
        
        self.assertEqual(response['status'], 'success')
        self.assertIn('event_id', response)
        self.assertIn('mock_event_', response['event_id'])
        self.assertEqual(response['details']['title'], 'Test Event')
        self.assertEqual(response['details']['organizer'], self.user.email)
    
    def test_check_availability_message(self):
        """Test the availability message generation."""
        # Without selected time
        message = MockGoogleCalendar.check_availability_message(self.meeting)
        self.assertEqual(message, "No time selected yet")
        
        # With selected time
        time_option = TimeOption.objects.create(
            meeting_request=self.meeting,
            start_time=timezone.now() + timedelta(days=1),
            end_time=timezone.now() + timedelta(days=1, hours=1),
            is_selected=True
        )
        
        message = MockGoogleCalendar.check_availability_message(self.meeting)
        self.assertIn('participants', message)
        self.assertTrue(message.startswith('✅') or message.startswith('⚠️'))
