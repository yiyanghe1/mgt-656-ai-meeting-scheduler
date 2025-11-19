from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('meetings/new/', views.create_meeting, name='create_meeting'),
    path('meetings/<int:pk>/', views.MeetingDetailView.as_view(), name='meeting_detail'),
    path('meetings/<int:pk>/select-time/', views.select_time, name='select_time'),
]
