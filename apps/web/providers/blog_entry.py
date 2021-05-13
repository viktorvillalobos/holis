from ..models import BlogEntry


def get_blog_entry_by_slug(slug: str) -> BlogEntry:
    return BlogEntry.objects.get(slug=slug, is_draft=False)
