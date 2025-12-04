# mgt-656-ai-meeting-scheduler
Code base for an AI event scheduling app that syncs with Google calendar to find available meeting times between contacts.

## 🚀 Sprint 3 MVP Complete!

We've successfully implemented a functional meeting scheduling application with user authentication, meeting management, and mock Google Calendar integration.

### Features Implemented in Sprint 3

- **User Authentication**: Complete signup, login, and logout functionality
- **Meeting Management**: Create and manage meeting requests with multiple time slots
- **User Dashboard**: View all your meetings in one place
- **Time Selection**: Choose the final meeting time from proposed options
- **Mock Calendar Integration**: Simulated Google Calendar (ready for real API in Sprint 4)

### Project Structure

```
├── ai_event_scheduler/     # Main Django project settings
├── homepage/              # Landing page app
├── scheduler/             # Core scheduling app (NEW!)
│   ├── models.py         # MeetingRequest & TimeOption models
│   ├── views.py          # Meeting management views
│   ├── auth_views.py     # Authentication views
│   ├── templates/        # HTML templates
│   ├── integrations/     # Google Calendar mock
│   └── tests/            # Comprehensive test suite
├── docs/sprints/          # Sprint documentation
└── manage.py             # Django management

### Instructions for testing locally

1. **Install dependencies:**
   ```bash
   python -m pip install -r requirements.txt
   ```
   
   **Note for Windows users:** If `pip` is not recognized, use `python -m pip` instead. Alternatively, you can use `py -m pip` (Python launcher).

2. **Set up PostgreSQL database:**
   - Connect to our database (name: `ai-event-scheduler-db`) locally using the external database URL
   - This can be found in database settings on our Render project
   - In your terminal, run the command in the comment below, replacing external_db_url with the actual database URL:
   **$env:DATABASE_URL="external_db_url"**

3. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

4. **Start the development server:**
   ```bash
   python manage.py runserver
   ```

5. **Visit the app:**
   - Open your browser and go to `http://127.0.0.1:8000/`
   - You'll see the landing page with options to Sign Up or Login
   
### Running Tests

```bash
# Run all tests
python manage.py test

# Run specific test modules
python manage.py test scheduler.test_auth
python manage.py test scheduler.test_views
python manage.py test scheduler.tests
```

### User Journey

1. **New User**: Homepage → Sign Up → Dashboard → Create Meeting → Add Time Slots → Select Time
2. **Returning User**: Homepage → Login → Dashboard → View/Manage Meetings

### Instructions for deploying to render

Follow the instructions at 'https://render.com/docs/deploy-django' to deploy the project to our staging environment.

All necessary dependencies should be included in the requirements.txt file

### View the staging app here

https://ai-event-scheduler-staging.onrender.com

# Meeting Scheduler

## Deployment
Prerequisites:
- Runtime: Node.js 20, Python 3.11, or Go 1.22 depending on the project parts.
- Backing services configured via environment variables (see .env.example).

Steps:
1. Copy .env.example to .env and set values.
2. Install dependencies:
   - Node: npm ci
   - Python: pip install -r requirements.txt or pip install .
   - Go: go mod download
3. Run migrations or setup scripts if applicable.
4. Start:
   - Node: PORT=${PORT:-3000} npm start
   - Python: PORT=${PORT:-8000} python -m your_app
   - Go: PORT=${PORT:-8080} go run ./cmd/your_app
5. Logs are written to stdout/stderr. Use your platform log collector.

## Testing
- Node: npm test
- Python: pytest
- Go: go test ./...

## Linting
- Node: npm run lint (configure eslint)
- Python: flake8 .
- Go: golangci-lint run

## 12-Factor Notes
- Config: only via environment variables, never hardcoded.
- Dependencies: declared in manifest (package.json, pyproject.toml/requirements.txt, go.mod) and lockfiles where applicable.
- Backing services: connect via URLs in env (e.g., DATABASE_URL, REDIS_URL).
- Build, release, run: separate; use CI/CD to build and deploy.
- Stateless processes: store state in external services.
- Port binding: respect PORT env var.
- Concurrency: scale via processes/instances.
- Logs: write to stdout/stderr.
- Admin tasks: run as one-off processes using the same codebase.