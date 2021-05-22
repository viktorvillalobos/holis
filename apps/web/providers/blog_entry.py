from ..models import BlogEntry


def get_blog_entry_by_slug(category_slug: str, slug: str) -> BlogEntry:
    return BlogEntry.objects.select_related("category").get(
        category__slug=category_slug, slug=slug, is_draft=False
    )
