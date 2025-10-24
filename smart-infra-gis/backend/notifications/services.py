from django.core.mail import send_mail
from django.conf import settings

def send_conflict_notification(conflict):
    """Send email notification when conflict is detected"""
    subject = f'New Conflict Detected: {conflict.project.name}'
    message = f'''
    A new conflict has been detected:

    Project: {conflict.project.name}
    Pipeline: {conflict.pipeline.name}
    Type: {conflict.conflict_type}
    Severity: {conflict.severity}

    Please review and take action.
    '''

    recipient_list = [conflict.project.created_by.email]

    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        recipient_list,
        fail_silently=True,
    )

def send_project_approval_notification(project):
    """Send notification when project is approved"""
    subject = f'Project Approved: {project.name}'
    message = f'''
    Your project has been approved:

    Project: {project.name}
    City: {project.city}
    Status: {project.status}

    You can now proceed with implementation.
    '''

    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [project.created_by.email],
        fail_silently=True,
    )