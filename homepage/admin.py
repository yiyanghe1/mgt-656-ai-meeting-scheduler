from django.contrib import admin
from .models import UserDetails, AbTestEvent, AbTestClickEvent

admin.site.register(UserDetails)
admin.site.register(AbTestEvent)
admin.site.register(AbTestClickEvent)

