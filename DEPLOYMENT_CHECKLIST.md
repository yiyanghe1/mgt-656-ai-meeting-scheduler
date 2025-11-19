# Deployment Checklist for Sprint 3

## Pre-Deployment Verification

### ✅ Code Readiness
- [x] All Sprint 3 features implemented
- [x] Tests passing locally
- [x] No hardcoded secrets in code
- [x] Environment variables documented
- [x] Database migrations created

### ✅ Required Environment Variables
Ensure these are set in your deployment environment:
- `DATABASE_URL` - PostgreSQL connection string
- `SECRET_KEY` - Django secret key (generate a new one for production)
- `DEBUG` - Set to False for production/staging

### ✅ Files Ready for Deployment
- [x] `requirements.txt` - All dependencies listed
- [x] `build.sh` - Build script for Render
- [x] `.flake8` - Linter configuration
- [x] Migration files in `scheduler/migrations/`

## Deployment Steps for Render

### 1. Database Setup
- PostgreSQL database is already configured on Render
- `DATABASE_URL` will be automatically set by Render

### 2. Environment Configuration
In Render Dashboard, set:
```
SECRET_KEY=<generate-a-secure-key>
PYTHON_VERSION=3.11.0
```

### 3. Build Command
The `build.sh` script handles:
- Installing dependencies
- Collecting static files
- Running migrations

### 4. Start Command
Already configured in project:
```
gunicorn ai_event_scheduler.wsgi:application
```

## Post-Deployment Testing

### 1. Verify Core Functionality
- [ ] Homepage loads
- [ ] User can sign up
- [ ] User can log in
- [ ] Dashboard accessible after login
- [ ] Can create meeting request
- [ ] Can select meeting time

### 2. Check Static Files
- [ ] CSS styling appears correctly
- [ ] Bootstrap resources load

### 3. Database Verification
- [ ] User creation works
- [ ] Meeting data persists
- [ ] Time selections save correctly

## Staging URL
https://ai-event-scheduler-staging.onrender.com

## Troubleshooting

### If migrations fail:
1. Check `DATABASE_URL` is set correctly
2. Verify database is accessible
3. Run `python manage.py migrate` manually

### If static files don't load:
1. Check `whitenoise` is installed
2. Verify `STATIC_ROOT` setting
3. Check `build.sh` ran successfully

### If authentication redirects fail:
1. Verify `LOGIN_URL` setting
2. Check `ALLOWED_HOSTS` includes your domain
3. Ensure `SESSION_COOKIE_SECURE` is appropriate for environment

## Sprint 3 Deployment Status
- [x] Code complete and tested
- [x] Documentation ready
- [ ] Deployed to staging (pending)
- [ ] Smoke tests passed (pending)
- [ ] Ready for demo (pending)
