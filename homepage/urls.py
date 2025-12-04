from django.urls import path
from . import views
import hashlib

_slug = hashlib.sha1(b"coffee-chatters").hexdigest()[:7]

urlpatterns = [
    path('', views.index, name='index'),
    path(f'{_slug}/', views.coffee_abtest, name='coffee_abtest'),
    path(f'{_slug}/track-click/', views.coffee_abtest_click, name='coffee_abtest_click'),
]

