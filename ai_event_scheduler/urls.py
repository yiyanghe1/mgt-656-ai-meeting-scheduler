"""
URL configuration for the ai_event_scheduler project.
"""
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from scheduler.auth_views import SignUpView, CustomLoginView, CustomLogoutView
from django.views.i18n import set_timezone  # ADD

def health_check(request):
    """Simple health check endpoint for monitoring."""
    return JsonResponse({'status': 'healthy', 'service': 'ai-event-scheduler'})

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



