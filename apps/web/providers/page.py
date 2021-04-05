from ..models import Page


def get_page_by_slug(slug: str) -> Page:
    return Page.objects.get(slug=slug, is_draft=False)
