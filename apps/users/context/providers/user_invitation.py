from ..models import UserInvitation


def create_users_invitations(
    company_id: int, user_id: int, emails: list[str]
) -> list[UserInvitation]:

    users = [
        UserInvitation(company_id=company_id, email=email, created_by_id=user_id)
        for email in emails
    ]

    return UserInvitation.objects.bulk_create(users)
