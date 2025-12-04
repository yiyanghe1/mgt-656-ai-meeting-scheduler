from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class MeetingRequest(models.Model):
    """
    Model representing a meeting request created by a user.
    """
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organized_meetings')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.title} - organized by {self.organizer.username}"
    
    @property
    def has_selected_time(self):
        """Check if any time option has been selected."""
        return self.time_options.filter(is_selected=True).exists()
    
    @property
    def selected_time(self):
        """Get the selected time option if any."""
        return self.time_options.filter(is_selected=True).first()


class TimeOption(models.Model):
    """
    Model representing a potential time slot for a meeting.
    """
    meeting_request = models.ForeignKey(MeetingRequest, on_delete=models.CASCADE, related_name='time_options')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_selected = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['start_time']
        
    def __str__(self):
        return f"{self.meeting_request.title}: {self.start_time.strftime('%Y-%m-%d %H:%M')} - {self.end_time.strftime('%Y-%m-%d %H:%M')}"
    
    def save(self, *args, **kwargs):
        # Ensure only one time option can be selected per meeting
        if self.is_selected:
            TimeOption.objects.filter(
                meeting_request=self.meeting_request,
                is_selected=True
            ).update(is_selected=False)
        super().save(*args, **kwargs)
        
    @property
    def duration_minutes(self):
        """Calculate duration in minutes."""
        delta = self.end_time - self.start_time
        return int(delta.total_seconds() / 60)


class GoogleOAuthCredential(models.Model):
    """Per-user Google OAuth credential storage."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='google_oauth')
    token = models.TextField()
    refresh_token = models.TextField(blank=True, null=True)
    token_uri = models.CharField(max_length=255, default='https://oauth2.googleapis.com/token')
    scopes = models.TextField(blank=True, default='')  # space-separated
    expiry = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'google_oauth_credentials'

    def __str__(self):
        return f"Google OAuth for {self.user.username}"
