from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from django.contrib import messages
from django.utils.dateparse import parse_datetime
from .models import MeetingRequest, TimeOption
from .integrations.google_calendar import MockGoogleCalendar, create_calendar_event
from django.conf import settings
from django.utils import timezone as dj_timezone
from zoneinfo import ZoneInfo
from .emails import send_meeting_created_email, send_time_selected_email
from django.urls import reverse
from .models import GoogleOAuthCredential

try:
    from google_auth_oauthlib.flow import Flow
    GOOGLE_OAUTH_AVAILABLE = True
except Exception:
    GOOGLE_OAUTH_AVAILABLE = False

@login_required
def dashboard(request):
    """Display user's dashboard with their meeting requests."""
    meetings = MeetingRequest.objects.filter(organizer=request.user)
    return render(request, 'scheduler/dashboard.html', {
        'meetings': meetings
    })


@login_required
def create_meeting(request):
    """Create a new meeting request with time options."""
    if request.method == 'POST':
        # Get form data
        title = request.POST.get('title')
        description = request.POST.get('description', '')
        
        # Create meeting request
        meeting = MeetingRequest.objects.create(
            organizer=request.user,
            title=title,
            description=description
        )
        
        # Process time slots
        time_slot_count = int(request.POST.get('time_slot_count', 0))
        for i in range(time_slot_count):
            start_time_str = request.POST.get(f'start_time_{i}')
            end_time_str = request.POST.get(f'end_time_{i}')
            
            if start_time_str and end_time_str:
                start_time = parse_datetime(start_time_str.replace('T', ' '))
                end_time = parse_datetime(end_time_str.replace('T', ' '))

                # Make times aware in user's timezone (then Django will store as UTC)
                if start_time and end_time:
                    tzname = request.session.get('django_timezone', settings.TIME_ZONE)
                    try:
                        tz = ZoneInfo(tzname)
                    except Exception:
                        tz = dj_timezone.utc
                    start_time = dj_timezone.make_aware(start_time, tz)
                    end_time = dj_timezone.make_aware(end_time, tz)
                
                if start_time and end_time and end_time > start_time:
                    TimeOption.objects.create(
                        meeting_request=meeting,
                        start_time=start_time,
                        end_time=end_time
                    )
        
        messages.success(request, 'Meeting request created successfully!')
        # Send organizer notification (best-effort, non-blocking)
        try:
            send_meeting_created_email(meeting)
        except Exception:
            pass
        return redirect('meeting_detail', pk=meeting.pk)
    
    return render(request, 'scheduler/create_meeting.html')


class MeetingDetailView(LoginRequiredMixin, DetailView):
    """Display meeting details."""
    model = MeetingRequest
    template_name = 'scheduler/meeting_detail.html'
    context_object_name = 'meeting'
    
    def get_queryset(self):
        """Ensure users can only see meetings they organized."""
        return MeetingRequest.objects.filter(organizer=self.request.user)
    
    def get_context_data(self, **kwargs):
        """Add Google Calendar availability info to context."""
        context = super().get_context_data(**kwargs)
        meeting = self.get_object()
        
        # Replace mock with dynamic check via integration wrapper
        from .integrations.google_calendar import check_availability_message
        context['availability_status'] = check_availability_message(meeting)
        context['google_connected'] = GoogleOAuthCredential.objects.filter(user=self.request.user).exists()
        
        return context


@login_required
def select_time(request, pk):
    """Select a time option for a meeting."""
    meeting = get_object_or_404(MeetingRequest, pk=pk, organizer=request.user)
    
    if request.method == 'POST':
        time_option_id = request.POST.get('time_option_id')
        time_option = get_object_or_404(TimeOption, pk=time_option_id, meeting_request=meeting)
        
        # Mark this option as selected (the model will handle unsetting others)
        time_option.is_selected = True
        time_option.save()
        
        # Simulate creating a calendar event (Sprint 3 - mocked)
        calendar_response = create_calendar_event(
            user=request.user,
            title=meeting.title,
            start_time=time_option.start_time,
            end_time=time_option.end_time,
            description=meeting.description or ""
        )
        
        if calendar_response['status'] == 'success':
            messages.success(
                request, 
                f'Time selected: {time_option.start_time.strftime("%Y-%m-%d %H:%M")}. '
                f'(Calendar event would be created - Event ID: {calendar_response["event_id"]})'
            )
        else:
            messages.success(request, f'Time selected: {time_option.start_time.strftime("%Y-%m-%d %H:%M")}')
        
        # Send organizer notification (best-effort, non-blocking)
        try:
            send_time_selected_email(meeting, time_option)
        except Exception:
            pass

        return redirect('meeting_detail', pk=meeting.pk)
    
    return redirect('meeting_detail', pk=meeting.pk)


@login_required
def delete_meeting(request, pk):
    """Delete a meeting request (organizer only)."""
    meeting = get_object_or_404(MeetingRequest, pk=pk, organizer=request.user)
    if request.method == 'POST':
        title = meeting.title
        meeting.delete()
        messages.success(request, f'Meeting "{title}" deleted.')
        return redirect('dashboard')
    return render(request, 'scheduler/confirm_delete.html', {'meeting': meeting})


@login_required
def google_connect(request):
    """Start OAuth flow to connect user's Google account."""
    if not GOOGLE_OAUTH_AVAILABLE:
        messages.error(request, 'Google OAuth libraries not installed.')
        return redirect('dashboard')

    redirect_uri = request.build_absolute_uri(reverse('google_oauth_callback'))
    scopes = getattr(settings, 'GOOGLE_OAUTH_SCOPES', [
        'https://www.googleapis.com/auth/calendar.readonly',
        'https://www.googleapis.com/auth/calendar.events',
    ])

    client_config = {
        'web': {
            'client_id': settings.GOOGLE_OAUTH_CLIENT_ID,
            'project_id': 'ai-event-scheduler',
            'auth_uri': 'https://accounts.google.com/o/oauth2/auth',
            'token_uri': 'https://oauth2.googleapis.com/token',
            'client_secret': settings.GOOGLE_OAUTH_CLIENT_SECRET,
            'redirect_uris': [redirect_uri],
        }
    }

    flow = Flow.from_client_config(client_config, scopes=scopes, redirect_uri=redirect_uri)
    auth_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true',
        prompt='consent',
    )
    request.session['google_oauth_state'] = state
    request.session['google_oauth_next'] = request.GET.get('next') or request.META.get('HTTP_REFERER') or reverse('dashboard')
    return redirect(auth_url)


@login_required
def google_oauth_callback(request):
    """Handle OAuth callback and save credentials."""
    if not GOOGLE_OAUTH_AVAILABLE:
        messages.error(request, 'Google OAuth libraries not installed.')
        return redirect('dashboard')

    redirect_uri = request.build_absolute_uri(reverse('google_oauth_callback'))
    scopes = getattr(settings, 'GOOGLE_OAUTH_SCOPES', [
        'https://www.googleapis.com/auth/calendar.readonly',
        'https://www.googleapis.com/auth/calendar.events',
    ])

    client_config = {
        'web': {
            'client_id': settings.GOOGLE_OAUTH_CLIENT_ID,
            'project_id': 'ai-event-scheduler',
            'auth_uri': 'https://accounts.google.com/o/oauth2/auth',
            'token_uri': 'https://oauth2.googleapis.com/token',
            'client_secret': settings.GOOGLE_OAUTH_CLIENT_SECRET,
            'redirect_uris': [redirect_uri],
        }
    }

    state = request.session.get('google_oauth_state')
    flow = Flow.from_client_config(client_config, scopes=scopes, state=state, redirect_uri=redirect_uri)
    try:
        flow.fetch_token(authorization_response=request.build_absolute_uri())
        creds = flow.credentials
        record, _ = GoogleOAuthCredential.objects.get_or_create(user=request.user)
        record.token = creds.token
        if getattr(creds, 'refresh_token', None):
            record.refresh_token = creds.refresh_token
        record.token_uri = getattr(creds, 'token_uri', 'https://oauth2.googleapis.com/token')
        record.expiry = getattr(creds, 'expiry', None)
        record.scopes = ' '.join(scopes)
        record.save()
        messages.success(request, 'Google Calendar connected successfully.')
    except Exception as e:
        messages.error(request, f'Failed to connect Google Calendar: {e}')

    next_url = request.session.pop('google_oauth_next', None) or reverse('dashboard')
    return redirect(next_url)


@login_required
def google_disconnect(request):
    """Disconnect and remove stored Google OAuth credentials."""
    try:
        GoogleOAuthCredential.objects.filter(user=request.user).delete()
        messages.success(request, 'Google Calendar disconnected.')
    except Exception:
        messages.error(request, 'Failed to disconnect Google Calendar.')
    next_url = request.GET.get('next') or request.META.get('HTTP_REFERER') or reverse('dashboard')
    return redirect(next_url)
