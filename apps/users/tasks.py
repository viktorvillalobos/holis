from typing import Any

from celery import shared_task
from django.contrib.auth import get_user_model

User = get_user_model()


@shared_task()
def get_users_count():
    """A pointless Celery task to demonstrate usage."""
    return User.objects.count()


@shared_task()
def send_users_invitations(invitations: list[dict[str, Any]]) -> list[str]:
    """
        Send emails to the users to accept the values
    """
    # TODO: Send emails

    return [invitation.email for invitation in invitations]
