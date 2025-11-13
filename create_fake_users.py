"""
Script to create five fake user records for UserDetails model.
Run with: python manage.py shell < create_fake_users.py
Or: python create_fake_users.py
"""
import os
import django
from datetime import datetime, timezone

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai_event_scheduler.settings')
django.setup()

from homepage.models import UserDetails

# Create five fake users with generic names
fake_users = [
    {
        'firstname': 'John',
        'lastname': 'Doe',
        'google_account': 'john.doe@gmail.com'
    },
    {
        'firstname': 'Jane',
        'lastname': 'Smith',
        'google_account': 'jane.smith@gmail.com'
    },
    {
        'firstname': 'Bob',
        'lastname': 'Johnson',
        'google_account': 'bob.johnson@gmail.com'
    },
    {
        'firstname': 'Alice',
        'lastname': 'Williams',
        'google_account': 'alice.williams@gmail.com'
    },
    {
        'firstname': 'Charlie',
        'lastname': 'Brown',
        'google_account': 'charlie.brown@gmail.com'
    }
]

# Create timestamp (same for both first_auth_ts and last_auth_ts)
timestamp = datetime.now(timezone.utc)

# Create and save users
created_users = []
for user_data in fake_users:
    user = UserDetails(
        firstname=user_data['firstname'],
        lastname=user_data['lastname'],
        google_account=user_data['google_account'],
        first_auth_ts=timestamp,
        last_auth_ts=timestamp
    )
    # Save the user (explicitly set values will override auto_now/auto_now_add)
    user.save()
    # Update timestamps again after save to ensure they match (in case auto_now overwrote last_auth_ts)
    UserDetails.objects.filter(userID=user.userID).update(
        first_auth_ts=timestamp,
        last_auth_ts=timestamp
    )
    user.refresh_from_db()
    created_users.append(user)
    print(f"Created user: {user} (first_auth: {user.first_auth_ts}, last_auth: {user.last_auth_ts})")

print(f"\nSuccessfully created {len(created_users)} fake users!")

