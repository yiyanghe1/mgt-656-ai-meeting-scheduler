# Sprint 2 Planning

## Sprint Goal
Deploy a working web application to staging with basic framework setup, database connectivity, and at least one dynamic page demonstrating end-to-end functionality.

## Duration
2 weeks (Sprint 2)
**Start Date:** October 23, 2025  
**End Date:** November 5, 2025

## Team Members
- [Team Member 1]
- [Team Member 2]
- [Team Member 3]
- [Team Member 4]

## User Stories

### 1. Django Framework Setup (5 points)
**As a** developer  
**I want to** set up Django project structure with proper configuration  
**So that** we have a solid foundation for building the application  
**Assigned to:** [Team Member 1]

**Acceptance Criteria:**
- Django project initialized with proper structure
- Settings configured for development and staging
- Static files and media handling configured
- Basic URL routing established
- Project can run locally

### 2. PostgreSQL Database Configuration (5 points)
**As a** developer  
**I want to** configure PostgreSQL database connection  
**So that** the application can store and retrieve data  
**Assigned to:** [Team Member 2]

**Acceptance Criteria:**
- PostgreSQL database created and accessible
- Database connection configured in Django settings
- Environment variables for database credentials
- Database migrations can run successfully
- Connection tested and verified

### 3. Homepage with Dynamic Data (5 points)
**As a** user  
**I want to** see a homepage that displays data from the database  
**So that** I can verify the application is working end-to-end  
**Assigned to:** [Team Member 3]

**Acceptance Criteria:**
- Homepage route created and accessible
- Template renders user data from database
- Data is fetched dynamically (not hardcoded)
- Displays at least 5 users from UserDetails table
- Responsive design with basic styling

### 4. UserDetails Model and Migration (3 points)
**As a** developer  
**I want to** create a UserDetails model with migrations  
**So that** we can store user information in the database  
**Assigned to:** [Team Member 4]

**Acceptance Criteria:**
- UserDetails model created with required fields
- Database migration created and applied
- Model can store firstname, lastname, google_account
- Model includes timestamps (first_auth_ts, last_auth_ts)

### 5. Sample Data Script (2 points)
**As a** developer  
**I want to** create a script to populate sample user data  
**So that** we can test the homepage functionality  
**Assigned to:** [Team Member 1]

**Acceptance Criteria:**
- Script creates fake user data
- Can be run via command line
- Creates at least 10 sample users
- Data is realistic and varied

### 6. Staging Deployment (5 points)
**As a** developer  
**I want to** deploy the application to a staging environment  
**So that** stakeholders can access and test the application  
**Assigned to:** [Team Member 2]

**Acceptance Criteria:**
- Application deployed to Render (or similar platform)
- Staging URL is publicly accessible
- Database connection works in staging
- Application runs without errors
- Environment variables properly configured

### 7. Development Workflow Setup (3 points)
**As a** developer  
**I want to** establish version control best practices  
**So that** the team can collaborate effectively  
**Assigned to:** [Team Member 3]

**Acceptance Criteria:**
- Feature branch workflow established
- Pull request template created
- Code review process defined
- Meaningful commit messages used
- .gitignore properly configured

### 8. Initial Test Suite (3 points)
**As a** developer  
**I want to** write basic tests for core functionality  
**So that** we can verify the application works correctly  
**Assigned to:** [Team Member 4]

**Acceptance Criteria:**
- Test for database connection
- Test for homepage view
- Test for UserDetails model
- At least 3-5 test cases
- All tests passing

## Technical Tasks
1. Initialize Django project (`django-admin startproject`)
2. Create homepage app (`python manage.py startapp homepage`)
3. Configure PostgreSQL in settings.py
4. Create UserDetails model
5. Create and run migrations
6. Create homepage view and template
7. Set up URL routing
8. Create sample data script
9. Configure Render deployment
10. Set up environment variables
11. Write initial tests
12. Configure linting (flake8/black)

## Dependencies
- PostgreSQL database must be provisioned
- Render account and project created
- GitHub repository initialized
- Team members have development environment set up

## Risks and Mitigations

### Risk 1: Database Connection Issues
**Risk:** PostgreSQL connection might fail in staging environment  
**Mitigation:** Test database connection early, use environment variables, document connection string format

### Risk 2: Deployment Configuration
**Risk:** Render deployment might have configuration issues  
**Mitigation:** Follow Render documentation closely, test deployment early in sprint, have rollback plan

### Risk 3: Team Environment Setup
**Risk:** Team members might have different development environments  
**Mitigation:** Create setup documentation, use requirements.txt, provide clear instructions

### Risk 4: Time Constraints
**Risk:** Sprint 2 might be too ambitious for first development sprint  
**Mitigation:** Focus on core functionality (framework + database + one page), defer advanced features

## Definition of Done
- [ ] Django project structure created and configured
- [ ] PostgreSQL database connected and working
- [ ] Homepage displays dynamic data from database
- [ ] Application deployed to staging and accessible
- [ ] Sample data script works
- [ ] Initial tests written and passing
- [ ] Code committed to version control with proper workflow
- [ ] Documentation updated (README, deployment guide)
- [ ] Code reviewed by at least one team member
- [ ] No secrets hardcoded in code (environment variables used)

## Sprint Capacity
- **Total Story Points Committed:** 31 points
- **Team Velocity Estimate:** Based on team capacity and sprint duration
- **Buffer:** 10% for unexpected issues

