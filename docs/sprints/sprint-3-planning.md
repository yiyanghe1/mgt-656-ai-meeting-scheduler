# Sprint 3 Planning

## Sprint Goal
Implement end-to-end meeting scheduling MVP with authentication and basic availability.

## Duration
2 weeks (Sprint 3)

## Team Members
- [Team Member 1]
- [Team Member 2]
- [Team Member 3]
- [Team Member 4]

## User Stories

### 1. User Authentication (8 points)
**As a** user  
**I want to** sign up, log in, and log out  
**So that** I can securely access my meeting requests  
**Assigned to:** [Team Member 1]

**Acceptance Criteria:**
- User can sign up with username, email, and password
- User can log in with credentials
- User can log out
- Protected pages redirect to login when not authenticated

### 2. Create Meeting Request (5 points)
**As a** logged-in user  
**I want to** create a meeting request with multiple time options  
**So that** I can find a suitable time for my meeting  
**Assigned to:** [Team Member 2]

**Acceptance Criteria:**
- User can enter meeting title and description
- User can add multiple time slot options
- Meeting is saved and associated with the user
- User is redirected to meeting detail page

### 3. View Meeting Dashboard (3 points)
**As a** logged-in user  
**I want to** see all my meeting requests  
**So that** I can manage my meetings  
**Assigned to:** [Team Member 3]

**Acceptance Criteria:**
- Dashboard shows list of user's meetings
- Each meeting shows title, date, and status
- User can click to view meeting details

### 4. Select Meeting Time (5 points)
**As a** meeting organizer  
**I want to** select a final time from the proposed options  
**So that** I can confirm when the meeting will occur  
**Assigned to:** [Team Member 4]

**Acceptance Criteria:**
- User can view all time options
- User can select one time as final
- Selected time is clearly marked
- System shows confirmation message

### 5. Mock Google Calendar Integration (3 points)
**As a** developer  
**I want to** create a mock Google Calendar integration  
**So that** we can simulate calendar functionality for Sprint 3  
**Assigned to:** [Team Member 1]

**Acceptance Criteria:**
- Mock functions for calendar operations
- Simulated availability checking
- Clear documentation that this is temporary

### 6. Comprehensive Testing (5 points)
**As a** developer  
**I want to** create comprehensive tests  
**So that** we ensure our MVP works correctly  
**Assigned to:** [Team Member 2]

**Acceptance Criteria:**
- Auth tests (signup, login, logout)
- Model tests
- View tests
- Integration tests

## Technical Tasks
1. Create Django scheduler app
2. Define models (MeetingRequest, TimeOption)
3. Implement authentication views
4. Create templates for all pages
5. Set up URL routing
6. Write test suite
7. Update documentation

## Dependencies
- PostgreSQL database must be configured
- Django project structure already in place
- Render deployment configuration ready

## Risks and Mitigations

### Risk 1: Google Calendar API Complexity
**Risk:** Full Google Calendar integration might be too complex for Sprint 3  
**Mitigation:** Using mocked integration for this sprint, will implement real integration in Sprint 4

### Risk 2: Authentication Security
**Risk:** Custom auth implementation might have security issues  
**Mitigation:** Using Django's built-in authentication system and following best practices

### Risk 3: Time Zone Handling
**Risk:** Meeting times across time zones could be confusing  
**Mitigation:** For Sprint 3, assuming all times in UTC, will add timezone support in future sprint

## Definition of Done
- [ ] All code is written and committed
- [ ] All tests pass
- [ ] Code is deployed to Render staging
- [ ] User can complete full journey (signup → create meeting → select time)
- [ ] Documentation is updated
- [ ] Code reviewed by at least one team member
