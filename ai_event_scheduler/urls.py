"""
URL configuration for the ai_event_scheduler project.
"""
from django.contrib import admin
from django.urls import path
from django.http import HttpResponse

def hello_world(request):
    """Simple view that prints Hello world"""
    return HttpResponse("Hello world! This is our AI Event Scheduler app.")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', hello_world),
]



