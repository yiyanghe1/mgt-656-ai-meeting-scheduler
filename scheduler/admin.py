from django.contrib import admin
from .models import MeetingRequest, TimeOption, GoogleOAuthCredential

# Register your models here.
admin.site.register(MeetingRequest)
admin.site.register(TimeOption)
admin.site.register(GoogleOAuthCredential)
