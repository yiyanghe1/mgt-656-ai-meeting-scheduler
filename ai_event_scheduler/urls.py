"""
URL configuration for the ai_event_scheduler project.
"""
from django.contrib import admin
from django.urls import path, include
from scheduler.auth_views import SignUpView, CustomLoginView, CustomLogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('homepage.urls')),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('', include('scheduler.urls')),
]



