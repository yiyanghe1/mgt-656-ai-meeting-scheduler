"""
Test script to verify database connection settings.
Run this to debug connection issues.
"""
import os
from urllib.parse import urlparse

database_url = os.environ.get('DATABASE_URL')

if not database_url:
    print("ERROR: DATABASE_URL environment variable is not set!")
    print("\nTo set it in PowerShell:")
    print('  $env:DATABASE_URL="postgresql://username:password@host:port/database_name"')
    print("\nTo set it in Command Prompt:")
    print('  set DATABASE_URL=postgresql://username:password@host:port/database_name')
    exit(1)

print("DATABASE_URL found!")
print(f"Full URL (password hidden): {database_url.split('@')[0].split(':')[0]}://***:***@{database_url.split('@')[1] if '@' in database_url else 'N/A'}")

parsed = urlparse(database_url)

print("\nParsed connection details:")
print(f"  Host: {parsed.hostname}")
print(f"  Port: {parsed.port or '5432'}")
print(f"  Database: {parsed.path[1:] if parsed.path else 'N/A'}")
print(f"  User: {parsed.username}")

# Check if it's an internal URL
if parsed.hostname and 'internal' in parsed.hostname.lower():
    print("\n⚠️  WARNING: This looks like an INTERNAL Database URL!")
    print("   Internal URLs only work from within Render's network.")
    print("   For local development, you need the EXTERNAL Database URL.")
    print("   Check your Render dashboard for the External Database URL.")

# Try to import Django and test connection
try:
    import django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai_event_scheduler.settings')
    django.setup()
    
    from django.db import connection
    print("\nAttempting to connect to database...")
    connection.ensure_connection()
    print("✅ SUCCESS: Database connection established!")
    
except Exception as e:
    print(f"\n❌ ERROR: Could not connect to database")
    print(f"   Error: {str(e)}")
    print("\nTroubleshooting steps:")
    print("1. Verify you're using the EXTERNAL Database URL (not Internal)")
    print("2. Check if your IP address is whitelisted in Render")
    print("3. Verify the database is running in Render dashboard")
    print("4. Check that SSL is properly configured (already added to settings.py)")

