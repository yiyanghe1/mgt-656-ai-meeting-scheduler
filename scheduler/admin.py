from django.contrib import admin
from .models import MeetingRequest, TimeOption

# Register your models here.
admin.site.register(MeetingRequest)
admin.site.register(TimeOption)
