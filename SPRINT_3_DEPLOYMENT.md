# Sprint 3 Deployment Instructions

## Step 1: Commit and Push to GitHub

### 1.1 Check Git Status
First, let's see what files have been added/modified:
```bash
git status
```

### 1.2 Add All Sprint 3 Files
```bash
# Add all new files
git add .

# Or if you want to be selective:
git add scheduler/
git add docs/sprints/
git add .flake8
git add DEPLOYMENT_CHECKLIST.md
git add SPRINT_3_DEPLOYMENT.md
```

### 1.3 Commit Sprint 3 Changes
```bash
git commit -m "feat(sprint-3): Complete MVP implementation

- Add user authentication (signup/login/logout)
- Implement meeting creation with time slots
- Add dashboard and meeting detail views  
- Create mock Google Calendar integration
- Add comprehensive test suite (24+ tests)
- Document sprint planning, review, and retrospective
- Add scheduler app with models, views, and templates
- Configure linting with flake8
- Update README with Sprint 3 features"
```

### 1.4 Push to GitHub
```bash
git push origin main
```

If you haven't set up the remote yet:
```bash
git remote add origin https://github.com/yiyanghe1/mgt-656-ai-meeting-scheduler.git
git push -u origin main
```

## Step 2: Deploy to Render

### 2.1 Update Render Environment Variables
In your Render dashboard (https://dashboard.render.com):

1. Go to your web service: `ai-event-scheduler-staging`
2. Navigate to "Environment" tab
3. Add/Update these environment variables:
   - `SECRET_KEY` = (generate a secure key, e.g., using Python: `import secrets; print(secrets.token_hex(32))`)
   - `PYTHON_VERSION` = 3.11.0
   - `DATABASE_URL` = (should already be set by Render)
   - `DEBUG` = False (for staging/production)

### 2.2 Trigger Deployment

**Option A: Automatic Deploy (if connected to GitHub)**
1. If Render is connected to your GitHub repo, it should auto-deploy when you push
2. Check the "Events" tab in Render to see deployment progress

**Option B: Manual Deploy**
1. In Render dashboard, click "Manual Deploy"
2. Select "Deploy latest commit"

### 2.3 Monitor Deployment
Watch the deployment logs for any errors:
- Check for successful dependency installation
- Verify static files are collected
- Ensure migrations run successfully

## Step 3: Post-Deployment Verification

### 3.1 Test Core Features
Once deployed, test at https://ai-event-scheduler-staging.onrender.com:

1. **Homepage** - Should show welcome message with Sign Up/Login buttons
2. **Sign Up** - Create a test account
3. **Login** - Verify authentication works
4. **Dashboard** - Check that it loads after login
5. **Create Meeting** - Test meeting creation with time slots
6. **Select Time** - Verify time selection works

### 3.2 Check for Common Issues

**If you see "Server Error (500)":**
- Check Render logs for the specific error
- Common issues:
  - Missing SECRET_KEY environment variable
  - Database connection issues
  - Missing migrations

**If static files (CSS) don't load:**
- Verify whitenoise is installed (it is in requirements.txt)
- Check that build.sh ran successfully
- Look for collectstatic output in build logs

**If you can't access admin:**
- SSH into Render service and create superuser:
  ```bash
  python manage.py createsuperuser
  ```

## Step 4: Create GitHub Project Board

After deployment, set up your GitHub Project:

1. Go to https://github.com/yiyanghe1/mgt-656-ai-meeting-scheduler
2. Click "Projects" tab → "New Project"
3. Choose "Basic Kanban" template
4. Add Sprint 3 completed stories (mark as Done)
5. Add Sprint 4 backlog items

## Troubleshooting Commands

If you need to debug on Render:

```bash
# Check Django settings
python manage.py check

# Verify database connection
python manage.py dbshell

# Run migrations manually
python manage.py migrate

# Create test data
python create_fake_users.py
```

## Success Checklist

- [ ] Code pushed to GitHub
- [ ] Render deployment successful
- [ ] Homepage loads with styling
- [ ] User can sign up
- [ ] User can log in
- [ ] Dashboard accessible
- [ ] Meeting creation works
- [ ] Time selection works
- [ ] No 500 errors

## Next Steps

Once deployed successfully:
1. Share the staging URL with your team/instructor
2. Create GitHub Project board
3. Prepare for Sprint 3 demo
4. Start planning Sprint 4 based on feedback

Good luck with your deployment! 🚀
