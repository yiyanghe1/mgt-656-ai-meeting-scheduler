# Sprint 3 Files Checklist

Before pushing to GitHub, verify these files are included:

## New Directories
- [ ] `scheduler/` - Complete Django app
- [ ] `scheduler/migrations/` - Database migrations
- [ ] `scheduler/templates/` - HTML templates
- [ ] `scheduler/templates/auth/` - Auth templates
- [ ] `scheduler/templates/scheduler/` - App templates
- [ ] `scheduler/integrations/` - Google Calendar mock
- [ ] `docs/sprints/` - Sprint documentation

## New Python Files
- [ ] `scheduler/__init__.py`
- [ ] `scheduler/apps.py`
- [ ] `scheduler/admin.py`
- [ ] `scheduler/models.py` - MeetingRequest, TimeOption models
- [ ] `scheduler/views.py` - Main views
- [ ] `scheduler/auth_views.py` - Authentication views
- [ ] `scheduler/forms.py` - SignUpForm
- [ ] `scheduler/urls.py` - URL routing
- [ ] `scheduler/tests.py` - Model tests
- [ ] `scheduler/test_auth.py` - Auth tests
- [ ] `scheduler/test_views.py` - View tests
- [ ] `scheduler/test_integration.py` - Integration tests
- [ ] `scheduler/integrations/__init__.py`
- [ ] `scheduler/integrations/google_calendar.py` - Mock integration
- [ ] `scheduler/migrations/__init__.py`
- [ ] `scheduler/migrations/0001_initial.py` - Initial migration

## New Templates
- [ ] `scheduler/templates/auth/login.html`
- [ ] `scheduler/templates/auth/signup.html`
- [ ] `scheduler/templates/scheduler/dashboard.html`
- [ ] `scheduler/templates/scheduler/create_meeting.html`
- [ ] `scheduler/templates/scheduler/meeting_detail.html`

## New Documentation
- [ ] `docs/sprints/sprint-3-planning.md`
- [ ] `docs/sprints/sprint-3-review.md`
- [ ] `docs/sprints/sprint-3-retrospective.md`
- [ ] `docs/sprints/sprint-3-report.md`
- [ ] `docs/sprints/github-project-tasks.md`
- [ ] `scheduler/README.md`
- [ ] `DEPLOYMENT_CHECKLIST.md`
- [ ] `SPRINT_3_DEPLOYMENT.md`
- [ ] `SPRINT_3_FILES_CHECKLIST.md`

## Modified Files
- [ ] `ai_event_scheduler/settings.py` - Added scheduler app, auth settings
- [ ] `ai_event_scheduler/urls.py` - Added auth and scheduler URLs
- [ ] `homepage/templates/render/index.html` - Updated with navigation
- [ ] `requirements.txt` - Added flake8
- [ ] `README.md` - Updated with Sprint 3 info

## New Configuration
- [ ] `.flake8` - Linter configuration

## Total New Files: ~40+ files

Run `git status` to see all changes. If any files are missing, add them before committing.
