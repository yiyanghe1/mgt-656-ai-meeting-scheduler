from django.core.mail import send_mail
from django.utils import timezone

def _send(to_email: str, subject: str, message: str) -> None:
    """Safe send wrapper that no-ops if email missing."""
    if not to_email:
        return
    send_mail(
        subject=subject,
        message=message,
        from_email=None,  # uses DEFAULT_FROM_EMAIL
        recipient_list=[to_email],
        fail_silently=True,  # avoid breaking user flow if email fails
    )

def send_meeting_created_email(meeting) -> None:
    """Notify organizer after meeting creation with proposed options."""
    user = meeting.organizer
    subject = f"[AI Event Scheduler] Meeting created: {meeting.title}"
    lines = [
        f"Hi {user.first_name or user.username},",
        "",
        f"Your meeting '{meeting.title}' has been created.",
    ]
    if meeting.description:
        lines.append(f"Description: {meeting.description}")
    lines.append("")
    lines.append("Proposed time options:")
    options = list(meeting.time_options.order_by('start_time'))
    if not options:
        lines.append("- (no valid time options were added)")
    else:
        for opt in options:
            start = timezone.localtime(opt.start_time)
            end = timezone.localtime(opt.end_time)
            lines.append(f"- {start.strftime('%Y-%m-%d %H:%M')} to {end.strftime('%H:%M')} ({opt.duration_minutes} mins)")
    lines.extend([
        "",
        "You can manage this meeting from your dashboard.",
    ])
    _send(user.email, subject, "\n".join(lines))

def send_time_selected_email(meeting, selected_time) -> None:
    """Notify organizer after selecting the final time."""
    user = meeting.organizer
    subject = f"[AI Event Scheduler] Time selected for: {meeting.title}"
    start = timezone.localtime(selected_time.start_time)
    end = timezone.localtime(selected_time.end_time)
    message = "\n".join([
        f"Hi {user.first_name or user.username},",
        "",
        f"You selected a final time for '{meeting.title}':",
        f"- {start.strftime('%Y-%m-%d %H:%M')} to {end.strftime('%H:%M')} ({selected_time.duration_minutes} mins)",
        "",
        "This time is now marked as selected in your meeting details.",
    ])
    _send(user.email, subject, message)
