# Sprint 4 Retrospective

What went well:
- Calendar integration scope clarified; OAuth and sync flows designed
- A/B endpoint spec solid; bucketing/analytics plan ready
- Deployment pipeline and rollback plan documented

What didn’t go well:
- Provider setup (Google/Email) added unexpected friction
- Timezone/DST edge cases required rework in UI and invites

What to improve for final submission period:
- Lock scope; require PM approval for changes
- Increase automated test coverage on calendar, email, timezone flows
- Tighten analytics event definitions and dashboards
- Earlier QA/PM/dev reviews before merge
- Daily prod health check with clear ownership

Action items (next 9 days until final submission):
- Finalize carryover stories — Owner: <PM> — Due: <date>
- Close P0/P1 bugs — Owner: <QA Lead> — Due: <date>
- Raise test coverage to <target %> — Owner: <Eng> — Due: <date>
- Complete analytics dashboard KPIs — Owner: <Data/Eng> — Due: <date>
- Validate A/B data quality — Owner: <Eng> — Due: <date>
- Harden OAuth tokens/refresh handling — Owner: <Backend> — Due: <date>
- Create release/demo runbook — Owner: <DevOps> — Due: <date>
- Prepare final submission docs and demo script — Owner: <PM/Eng> — Due: <date>

Project reflection (across all sprints, what we learned):
- Smaller stories improved predictability
- Feature flags enabled safer releases
- Early CI/CD investment reduced integration pain
- Clear acceptance criteria cut rework
- Plan instrumentation and provider setup alongside features
