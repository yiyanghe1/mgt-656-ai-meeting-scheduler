# Scheduler App - AI Event Scheduler MVP

This Django app provides the core meeting scheduling functionality for Sprint 3.

## Features Implemented

### Authentication
- User signup with email
- Login/logout functionality  
- Protected views requiring authentication

### Meeting Management
- Create meeting requests with title and description
- Add multiple time slot options
- View all your meetings in a dashboard
- Select final meeting time from options

### Google Calendar (Mocked)
- Mock integration for availability checking
- Simulated calendar event creation
- Ready for real API integration in Sprint 4

## Project Structure

```
scheduler/
├── migrations/          # Database migrations
├── integrations/        # External service integrations
│   └── google_calendar.py  # Mock Google Calendar API
├── templates/           # HTML templates
│   ├── auth/           # Login/signup templates
│   └── scheduler/      # Meeting management templates
├── models.py           # MeetingRequest, TimeOption models
├── views.py            # Main scheduler views
├── auth_views.py       # Authentication views
├── forms.py            # Django forms
├── urls.py             # URL routing
├── tests.py            # Model tests
├── test_auth.py        # Authentication tests
├── test_views.py       # View tests
└── test_integration.py # Integration tests
```

## Running the Application

1. **Set up environment variables:**
   ```bash
   export DATABASE_URL="your_postgres_url"
   export SECRET_KEY="your_secret_key"
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

4. **Create a superuser (optional):**
   ```bash
   python manage.py createsuperuser
   ```

5. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

6. **Access the application:**
   - Homepage: http://localhost:8000/
   - Admin: http://localhost:8000/admin/
   - Login: http://localhost:8000/login/
   - Signup: http://localhost:8000/signup/
   - Dashboard: http://localhost:8000/dashboard/ (requires login)

## Running Tests

```bash
# Run all tests
python manage.py test

# Run specific test modules
python manage.py test scheduler.test_auth
python manage.py test scheduler.test_views
python manage.py test scheduler.test_integration
```

## User Journey

1. **New User:**
   - Visit homepage → Sign Up → Create account
   - Redirected to Dashboard
   - Create Meeting Request → Add time slots
   - View meeting details → Select preferred time
   - See mock calendar integration status

2. **Returning User:**
   - Visit homepage → Login
   - See dashboard with existing meetings
   - Create new meetings or manage existing ones

## API Endpoints

- `GET /` - Homepage
- `GET/POST /signup/` - User registration
- `GET/POST /login/` - User login
- `POST /logout/` - User logout
- `GET /dashboard/` - User's meeting dashboard (auth required)
- `GET/POST /meetings/new/` - Create meeting (auth required)
- `GET /meetings/<id>/` - Meeting details (auth required)
- `POST /meetings/<id>/select-time/` - Select meeting time (auth required)

## Future Enhancements (Sprint 4+)

1. **Real Google Calendar Integration**
   - OAuth2 authentication
   - Actual availability checking
   - Calendar event creation

2. **Participant Management**
   - Invite multiple attendees
   - Track RSVPs
   - Send email notifications

3. **Enhanced Features**
   - Timezone support
   - Recurring meetings
   - Meeting templates
   - Conflict resolution
   - Email reminders

## Notes for Developers

- The Google Calendar integration is currently mocked in `integrations/google_calendar.py`
- All times are currently stored in UTC
- Form validation is basic and can be enhanced
- The UI uses Bootstrap 4.5 for styling
- Tests cover the main user flows but edge cases need more coverage
