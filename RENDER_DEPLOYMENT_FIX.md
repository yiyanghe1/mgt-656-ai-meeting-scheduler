# Fixing 502 Bad Gateway Error on Render

## Changes Made to Fix the Issue:

### 1. Updated Settings (`ai_event_scheduler/settings.py`)
- Added fallback for SECRET_KEY (temporary, should be set in env vars)
- Fixed ALLOWED_HOSTS to include `mgt-656-ai-meeting-scheduler.onrender.com`
- Added proper DEBUG setting from environment
- Added database fallback for local development
- Added logging configuration for better debugging

### 2. Updated Build Script (`build.sh`)
- Added pip upgrade step
- Added --no-input flags to prevent hanging
- Added cache table creation (optional)

### 3. Added Deployment Files
- `render.yaml` - Render-specific configuration
- `Procfile` - Specifies how to start the app

## Next Steps:

### 1. Push These Changes to GitHub
```bash
git add .
git commit -m "fix: Resolve 502 Bad Gateway error on Render deployment"
git push origin main
```

### 2. Check Render Environment Variables
Go to your Render dashboard and ensure these are set:
- `SECRET_KEY` - A secure random string (or use generateValue)
- `DATABASE_URL` - Should be automatically set by Render
- `PYTHON_VERSION` - Set to 3.11.0

### 3. Trigger a New Deploy
After pushing, Render should automatically redeploy. If not:
1. Go to Render dashboard
2. Click "Manual Deploy"
3. Deploy latest commit

### 4. Monitor the Logs
In Render dashboard, go to "Logs" tab and look for:
- Build errors
- Database connection errors
- Missing environment variables
- Port binding issues

## Common Issues and Solutions:

### If SECRET_KEY Error:
```
Error: SECRET_KEY not set
```
**Solution**: Add SECRET_KEY to Render environment variables

### If Database Error:
```
django.db.utils.OperationalError: connection failed
```
**Solution**: Verify DATABASE_URL is set and PostgreSQL addon is attached

### If Module Import Error:
```
ModuleNotFoundError: No module named 'scheduler'
```
**Solution**: Ensure all files are committed and pushed to GitHub

### If Static Files Error:
```
ValueError: Missing staticfiles manifest
```
**Solution**: Check if collectstatic ran successfully in build logs

## Debugging Commands:

If you have shell access in Render:
```bash
# Check environment variables
env | grep -E '(SECRET_KEY|DATABASE_URL|DEBUG)'

# Test database connection
python manage.py dbshell

# Check Django configuration
python manage.py check --deploy

# Run migrations manually
python manage.py migrate --verbosity=3
```

## Expected Successful Deploy Log:
```
==> Building...
==> Installing dependencies with pip...
==> Running build command './build.sh'...
==> Collecting static files...
==> Running migrations...
==> Build successful 🎉
==> Starting service with 'gunicorn ai_event_scheduler.wsgi:application'
==> Your service is live 🎉
```

Once these changes are deployed, your app should be accessible at:
https://mgt-656-ai-meeting-scheduler.onrender.com
