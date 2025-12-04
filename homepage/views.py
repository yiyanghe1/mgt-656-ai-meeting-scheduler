from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import UserDetails, AbTestEvent, AbTestClickEvent
import random

def index(request):
    # Fetch the first 5 users from the database
    users = UserDetails.objects.all()[:5]
    context = {
        'users': users
    }
    return render(request, 'render/index.html', context)

TEAM_NICKNAMES = [
    'Alpha', 'Bravo', 'Charlie', 'Delta', 'Echo'
]

def coffee_abtest(request):
    """Public A/B test page for coffee-chatters."""
    if not request.session.session_key:
        request.session.save()

    variant = request.session.get('ab_variant')
    if variant not in ['kudos', 'thanks']:
        variant = random.choice(['kudos', 'thanks'])
        request.session['ab_variant'] = variant

    # Track every view
    AbTestEvent.objects.create(
        session_key=request.session.session_key,
        variant=variant,
        user_agent=request.META.get('HTTP_USER_AGENT', '')[:255],
        ip_address=request.META.get('REMOTE_ADDR', '')
    )

    return render(request, 'render/coffee_abtest.html', {
        'nicknames': TEAM_NICKNAMES,
        'variant': variant
    })

@require_POST
def coffee_abtest_click(request):
    """AJAX endpoint to record a button click for the A/B test."""
    if not request.session.session_key:
        request.session.save()
    variant = request.session.get('ab_variant')
    AbTestClickEvent.objects.create(
        session_key=request.session.session_key,
        variant=variant,
        user_agent=request.META.get('HTTP_USER_AGENT', '')[:255],
        ip_address=request.META.get('REMOTE_ADDR', '')
    )
    return JsonResponse({'status': 'ok', 'variant': variant})

