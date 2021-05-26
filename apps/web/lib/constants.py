from django.db.models import TextChoices


class BlogEntryLangChoices(TextChoices):
    EN = "en", "English"
    ES = "es", "Spanish"
