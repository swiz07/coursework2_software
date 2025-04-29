from django import template
from health_check.models import Session

register = template.Library()

@register.filter
def lookup_session_date(pk):
    """Return a friendly date/time for a session ID."""
    try:
        s = Session.objects.get(pk=pk)
        return s.date.strftime("%d/%m/%Y %I:%M %p")
    except Session.DoesNotExist:
        return ""

@register.filter
def lookup_session_status(pk):
    """Return 'Active' or 'Inactive' for a session ID."""
    try:
        return Session.objects.get(pk=pk).get_status_display()
    except Session.DoesNotExist:
        return ""
