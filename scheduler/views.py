from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from django.contrib import messages
from django.utils.dateparse import parse_datetime
from .models import MeetingRequest, TimeOption
from .integrations.google_calendar import MockGoogleCalendar, create_calendar_event


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
                
                if start_time and end_time and end_time > start_time:
                    TimeOption.objects.create(
                        meeting_request=meeting,
                        start_time=start_time,
                        end_time=end_time
                    )
        
        messages.success(request, 'Meeting request created successfully!')
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
        
        # Add mock Google Calendar availability status
        context['availability_status'] = MockGoogleCalendar.check_availability_message(meeting)
        
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
        
        return redirect('meeting_detail', pk=meeting.pk)
    
    return redirect('meeting_detail', pk=meeting.pk)
