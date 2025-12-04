"""
URL configuration for the ai_event_scheduler project.
"""
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.decorators.http import require_POST
from scheduler.auth_views import SignUpView, CustomLoginView, CustomLogoutView

def health_check(request):
    """Simple health check endpoint for monitoring."""
    return JsonResponse({'status': 'healthy', 'service': 'ai-event-scheduler'})

@require_POST
def set_timezone(request):
    """
    Set the timezone for the current session.
    This view stores the timezone in the session, which is then used by TimezoneMiddleware.
    """
    next_url = request.POST.get('next', '/')
    timezone_str = request.POST.get('timezone')
    
    if timezone_str:
        # Validate timezone by trying to create a ZoneInfo object
        try:
            from zoneinfo import ZoneInfo
            # This will raise an exception if the timezone is invalid
            ZoneInfo(timezone_str)
            # Store in session for TimezoneMiddleware
            request.session['django_timezone'] = timezone_str
        except Exception:
            # If timezone is invalid, just keep the current one
            pass
    
    return redirect(next_url)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('health/', health_check, name='health_check'),  # Health check endpoint
    path('tz/set/', set_timezone, name='set_timezone'),  # ADD: per-user timezone setter
    path('', include('homepage.urls')),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('', include('scheduler.urls')),
]