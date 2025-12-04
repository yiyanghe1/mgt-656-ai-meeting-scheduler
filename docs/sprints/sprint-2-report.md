# Sprint 2 Report: Foundation & Initial Deployment

**Team**: AI Event Scheduler Team  
**Sprint Duration**: October 23 - November 5, 2025  
**Report Date**: November 5, 2025

---

## 1. Sprint Goal & Achievement

### Sprint Goal
"Deploy a working web application to staging with basic framework setup, database connectivity, and at least one dynamic page demonstrating end-to-end functionality."

### Achievement Status: ✅ ACHIEVED
We successfully met our sprint goal by establishing a solid technical foundation. The Django application is deployed to staging, connected to PostgreSQL, and demonstrates dynamic data retrieval through a functional homepage. This "Hello World" sprint proves our technical setup works end-to-end.

---

## 2. Deployment

### Staging Application
**URL:** https://ai-event-scheduler-staging.onrender.com

### What's Working
- **Homepage**: Displays a welcome message and dynamically fetches user data from PostgreSQL database
- **Database Connection**: Successfully connected to PostgreSQL, can query and display UserDetails
- **Dynamic Content**: Homepage shows first 5 users from database in a formatted table
- **Responsive Design**: Basic Bootstrap styling for mobile-friendly display
- **Navigation**: Basic navigation structure in place

### Technical Stack Verified
- ✅ Django framework properly configured
- ✅ PostgreSQL database connected and accessible
- ✅ Environment variables configured (no secrets in code)
- ✅ Static files serving correctly
- ✅ Application runs without errors

---

## 3. Completed Work

### User Stories Completed (Total: 31 Story Points)

1. **Django Framework Setup** (5 points) - COMPLETED
   - Django project initialized with proper structure
   - Settings configured for development and staging environments
   - Static files and media handling configured
   - URL routing established
   - Project runs successfully locally and in staging

2. **PostgreSQL Database Configuration** (5 points) - COMPLETED
   - PostgreSQL database created and accessible
   - Database connection configured in Django settings
   - Environment variables for database credentials implemented
   - Database migrations run successfully
   - Connection tested and verified in both local and staging

3. **Homepage with Dynamic Data** (5 points) - COMPLETED
   - Homepage route created and accessible at `/`
   - Template (`index.html`) renders user data from database
   - Data fetched dynamically using Django ORM
   - Displays first 5 users from UserDetails table
   - Responsive Bootstrap design implemented

4. **UserDetails Model and Migration** (3 points) - COMPLETED
   - UserDetails model created with required fields:
     - `userID` (AutoField, primary key)
     - `firstname`, `lastname`, `google_account` (CharField)
     - `first_auth_ts`, `last_auth_ts` (DateTimeField)
   - Database migration created and applied
   - Model properly configured with Meta options

5. **Sample Data Script** (2 points) - COMPLETED
   - `create_fake_users.py` script created
   - Can be run via command line: `python create_fake_users.py`
   - Creates realistic sample user data
   - Script documented in `INSERT_FAKE_USERS.md`

6. **Staging Deployment** (5 points) - COMPLETED
   - Application deployed to Render staging environment
   - Staging URL publicly accessible
   - Database connection works in staging
   - Application runs without errors
   - Environment variables properly configured via Render dashboard

7. **Development Workflow Setup** (3 points) - COMPLETED
   - Feature branch workflow established
   - Pull request process defined
   - Code review process in place
   - Meaningful commit messages used
   - `.gitignore` properly configured for Django project

8. **Initial Test Suite** (3 points) - COMPLETED
   - Test for database connection (`test_db_connection.py`)
   - Test for homepage view functionality
   - Test for UserDetails model operations
   - 5+ test cases written and passing
   - Test suite can be run via `python manage.py test`

---

## 4. Velocity Tracking

- **Sprint 2 Velocity**: 31 points (100% completion rate)
- **Average Velocity**: 31 points (first sprint baseline)

The team completed all 31 story points planned for Sprint 2, demonstrating strong execution and accurate estimation for the foundation sprint.

---

## 5. Technical Progress

### What's Working Well:
- **Django Setup**: Framework initialization was straightforward
- **Database Integration**: PostgreSQL connection established without major issues
- **Deployment Process**: Render deployment process was well-documented and smooth
- **Model Design**: UserDetails model provides good foundation for future user management
- **Development Workflow**: Version control practices established early

### Technical Foundation Established:
- ✅ Django project structure
- ✅ PostgreSQL database connection
- ✅ Environment variable configuration
- ✅ Staging deployment pipeline
- ✅ Basic test suite
- ✅ Development workflow

### Areas for Future Enhancement:
- User authentication system (planned for Sprint 3)
- Meeting scheduling functionality (planned for Sprint 3)
- Enhanced UI/UX design
- More comprehensive test coverage
- CI/CD pipeline automation
- Production deployment configuration

---

## 6. Sprint Retrospective Highlights

### Key Insights:
1. **Foundation First**: Establishing the technical foundation early was critical for future sprints
2. **Deployment Early**: Getting staging deployment working early helped identify configuration issues
3. **Simple is Better**: Focusing on one working page with dynamic data proved the concept
4. **Documentation Matters**: Good documentation helped team members get up to speed quickly

### Action Items:
| Action | Owner | Deadline |
|--------|-------|----------|
| Set up user authentication system | TBD | Sprint 3 Week 1 |
| Create meeting scheduling models | TBD | Sprint 3 Week 1 |
| Enhance homepage design | TBD | Sprint 3 Week 1 |
| Expand test coverage | TBD | Sprint 3 Week 2 |
| Set up CI/CD pipeline | TBD | Sprint 3 Week 2 |

---

## 7. Sprint 3 Preview

### Priorities for Next Sprint:
1. **User Authentication**: Implement signup, login, and logout functionality
2. **Meeting Models**: Create MeetingRequest and TimeOption models
3. **Meeting Creation**: Build form and view for creating meeting requests
4. **User Dashboard**: Create dashboard to view user's meetings
5. **Mock Calendar Integration**: Create placeholder for Google Calendar integration
6. **Comprehensive Testing**: Expand test suite for new functionality

### Technical Debt to Address:
- Add more comprehensive error handling
- Improve form validation
- Enhance UI/UX design
- Add logging and monitoring
- Optimize database queries

---

## 8. Links

### Sprint Documentation:
- [Sprint 2 Planning](./sprint-2-planning.md)
- [Sprint 2 Review](./sprint-2-review.md)
- [Sprint 2 Retrospective](./sprint-2-retrospective.md)

### Code Repository:
- GitHub: https://github.com/yiyanghe1/mgt-656-ai-meeting-scheduler
- Staging URL: https://ai-event-scheduler-staging.onrender.com

### Project Management:
- GitHub Project Board: [To be created]
- Velocity Tracking: 31 points (Sprint 2)

---

## Summary

Sprint 2 successfully established the technical foundation for the AI Event Scheduler application. We deployed a working Django application to staging with PostgreSQL database connectivity and demonstrated end-to-end functionality through a dynamic homepage. With 100% story completion and a solid technical base, the team is well-positioned for Sprint 3's feature development.

The foundation is solid, and the path forward is clear: build user authentication, meeting scheduling functionality, and create a complete MVP in Sprint 3.

