from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from .models import MeetingRequest, TimeOption


class SchedulerViewsIntegrationTest(TestCase):
    """Integration tests for the complete meeting scheduling flow."""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        self.client.login(username='testuser', password='testpass123')
    
    def test_complete_meeting_flow(self):
        """Test the complete flow from creating to selecting a meeting time."""
        # 1. Create a meeting request
        response = self.client.post(reverse('create_meeting'), {
            'title': 'Team Planning Meeting',
            'description': 'Quarterly planning session',
            'time_slot_count': '2',
            'start_time_0': (timezone.now() + timedelta(days=1)).strftime('%Y-%m-%dT%H:%M'),
            'end_time_0': (timezone.now() + timedelta(days=1, hours=1)).strftime('%Y-%m-%dT%H:%M'),
            'start_time_1': (timezone.now() + timedelta(days=2)).strftime('%Y-%m-%dT%H:%M'),
            'end_time_1': (timezone.now() + timedelta(days=2, hours=2)).strftime('%Y-%m-%dT%H:%M'),
        })
        
        # Should redirect to meeting detail page
        self.assertEqual(response.status_code, 302)
        
        # 2. Verify meeting was created
        meeting = MeetingRequest.objects.get(title='Team Planning Meeting')
        self.assertEqual(meeting.organizer, self.user)
        self.assertEqual(meeting.time_options.count(), 2)
        self.assertFalse(meeting.has_selected_time)
        
        # 3. View meeting detail
        response = self.client.get(reverse('meeting_detail', kwargs={'pk': meeting.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Team Planning Meeting')
        self.assertContains(response, 'Quarterly planning session')
        self.assertContains(response, 'Select This Time')
        
        # 4. Select a time
        time_option = meeting.time_options.first()
        response = self.client.post(
            reverse('select_time', kwargs={'pk': meeting.pk}),
            {'time_option_id': time_option.id}
        )
        
        # Should redirect back to detail page
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('meeting_detail', kwargs={'pk': meeting.pk}))
        
        # 5. Verify time was selected
        time_option.refresh_from_db()
        meeting.refresh_from_db()
        self.assertTrue(time_option.is_selected)
        self.assertTrue(meeting.has_selected_time)
        self.assertEqual(meeting.selected_time, time_option)
        
        # 6. View updated meeting detail
        response = self.client.get(reverse('meeting_detail', kwargs={'pk': meeting.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Selected')
        self.assertContains(response, 'Google Calendar Integration Status')
    
    def test_dashboard_shows_user_meetings(self):
        """Test that dashboard only shows user's own meetings."""
        # Create meetings for different users
        other_user = User.objects.create_user(username='other', password='pass')
        
        meeting1 = MeetingRequest.objects.create(
            organizer=self.user,
            title='My Meeting'
        )
        meeting2 = MeetingRequest.objects.create(
            organizer=other_user,
            title='Other User Meeting'
        )
        
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'My Meeting')
        self.assertNotContains(response, 'Other User Meeting')
    
    def test_create_meeting_with_invalid_times(self):
        """Test creating a meeting with end time before start time."""
        response = self.client.post(reverse('create_meeting'), {
            'title': 'Invalid Meeting',
            'time_slot_count': '1',
            'start_time_0': (timezone.now() + timedelta(days=1, hours=2)).strftime('%Y-%m-%dT%H:%M'),
            'end_time_0': (timezone.now() + timedelta(days=1)).strftime('%Y-%m-%dT%H:%M'),  # End before start
        })
        
        # Meeting should be created but without time options
        meeting = MeetingRequest.objects.get(title='Invalid Meeting')
        self.assertEqual(meeting.time_options.count(), 0)
    
    def test_unauthorized_access_to_other_user_meeting(self):
        """Test that users cannot access meetings they didn't organize."""
        other_user = User.objects.create_user(username='other', password='pass')
        other_meeting = MeetingRequest.objects.create(
            organizer=other_user,
            title='Private Meeting'
        )
        
        response = self.client.get(
            reverse('meeting_detail', kwargs={'pk': other_meeting.pk})
        )
        self.assertEqual(response.status_code, 404)
