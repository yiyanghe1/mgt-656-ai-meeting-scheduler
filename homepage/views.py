from django.shortcuts import render
from .models import UserDetails


def index(request):
    # Fetch the first 5 users from the database
    users = UserDetails.objects.all()[:5]
    context = {
        'users': users
    }
    return render(request, 'render/index.html', context)

