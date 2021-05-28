from ..models import BlogEntry


def get_blog_entry_by_slug(lang: str, slug: str) -> BlogEntry:
    return BlogEntry.objects.select_related("category").get(
        lang=lang, slug=slug, is_draft=False
    )
