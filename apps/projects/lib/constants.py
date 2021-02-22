from django.db.models import IntegerChoices


class ProjectKind(IntegerChoices):
    COMPANY = 1
    TEAM = 2
    PROJECT = 3
