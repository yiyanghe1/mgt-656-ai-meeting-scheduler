from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from .models import MeetingRequest, TimeOption


class MeetingRequestModelTest(TestCase):
    """Test the MeetingRequest model."""
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.meeting = MeetingRequest.objects.create(
            organizer=self.user,
            title='Test Meeting',
            description='A test meeting description'
        )
    
    def test_meeting_creation(self):
        """Test that a meeting can be created with valid data."""
        self.assertEqual(self.meeting.title, 'Test Meeting')
        self.assertEqual(self.meeting.organizer, self.user)
        self.assertIsNotNone(self.meeting.created_at)
    
    def test_meeting_str_method(self):
        """Test the string representation of a meeting."""
        expected = f"Test Meeting - organized by {self.user.username}"
        self.assertEqual(str(self.meeting), expected)
    
    def test_has_selected_time_property(self):
        """Test the has_selected_time property."""
        self.assertFalse(self.meeting.has_selected_time)
        
        # Add a time option and select it
        time_option = TimeOption.objects.create(
            meeting_request=self.meeting,
            start_time=timezone.now() + timedelta(days=1),
            end_time=timezone.now() + timedelta(days=1, hours=1),
            is_selected=True
        )
        self.assertTrue(self.meeting.has_selected_time)


class TimeOptionModelTest(TestCase):
    """Test the TimeOption model."""
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.meeting = MeetingRequest.objects.create(
            organizer=self.user,
            title='Test Meeting'
        )
    
    def test_time_option_creation(self):
        """Test creating a time option."""
        start = timezone.now() + timedelta(days=1)
        end = start + timedelta(hours=1)
        
        time_option = TimeOption.objects.create(
            meeting_request=self.meeting,
            start_time=start,
            end_time=end
        )
        
        self.assertEqual(time_option.meeting_request, self.meeting)
        self.assertEqual(time_option.duration_minutes, 60)
        self.assertFalse(time_option.is_selected)
    
    def test_only_one_selected_time(self):
        """Test that only one time option can be selected per meeting."""
        option1 = TimeOption.objects.create(
            meeting_request=self.meeting,
            start_time=timezone.now() + timedelta(days=1),
            end_time=timezone.now() + timedelta(days=1, hours=1),
            is_selected=True
        )
        
        option2 = TimeOption.objects.create(
            meeting_request=self.meeting,
            start_time=timezone.now() + timedelta(days=2),
            end_time=timezone.now() + timedelta(days=2, hours=1),
            is_selected=True
        )
        
        # Refresh option1 from database
        option1.refresh_from_db()
        self.assertFalse(option1.is_selected)
        self.assertTrue(option2.is_selected)


class SchedulerViewsTest(TestCase):
    """Test scheduler views."""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
    
    def test_dashboard_requires_login(self):
        """Test that dashboard requires authentication."""
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)
    
    def test_dashboard_with_login(self):
        """Test dashboard view with authenticated user."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
    
    def test_create_meeting_requires_login(self):
        """Test that create meeting requires authentication."""
        response = self.client.get(reverse('create_meeting'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)
    
    def test_meeting_detail_requires_login(self):
        """Test that meeting detail requires authentication."""
        meeting = MeetingRequest.objects.create(
            organizer=self.user,
            title='Test Meeting'
        )
        response = self.client.get(reverse('meeting_detail', kwargs={'pk': meeting.pk}))
        self.assertEqual(response.status_code, 302)
