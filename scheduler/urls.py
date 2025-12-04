from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('meetings/new/', views.create_meeting, name='create_meeting'),
    path('meetings/<int:pk>/', views.MeetingDetailView.as_view(), name='meeting_detail'),
    path('meetings/<int:pk>/select-time/', views.select_time, name='select_time'),
    path('meetings/<int:pk>/delete/', views.delete_meeting, name='delete_meeting'),
    # Google OAuth
    path('google/connect/', views.google_connect, name='google_connect'),
    path('google/oauth2/callback/', views.google_oauth_callback, name='google_oauth_callback'),
    path('google/disconnect/', views.google_disconnect, name='google_disconnect'),
]
