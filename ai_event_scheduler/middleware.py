"""
Custom middleware for handling timezone activation from session.
"""
from django.utils import timezone as dj_timezone
from django.conf import settings
from zoneinfo import ZoneInfo


class TimezoneMiddleware:
    """
    Middleware that activates a timezone for the current request based on session.
    The timezone should be stored in request.session['django_timezone'].
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get timezone from session, default to settings.TIME_ZONE
        tzname = request.session.get('django_timezone', settings.TIME_ZONE)
        
        # Activate the timezone for this request
        try:
            dj_timezone.activate(ZoneInfo(tzname))
        except Exception:
            # If timezone is invalid, fall back to default from settings
            try:
                dj_timezone.activate(ZoneInfo(settings.TIME_ZONE))
            except Exception:
                dj_timezone.activate(ZoneInfo('UTC'))
        
        return self.get_response(request)

