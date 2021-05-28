from django.template.defaultfilters import slugify

import pytest
from model_bakery import baker

from ...providers import blog_entry as blog_entry_providers


@pytest.mark.django_db
def test_get_blog_entry_by_slug(django_assert_num_queries):
    blog_category = baker.make("web.BlogCategory")
    blog_entry = baker.make(
        "web.BlogEntry", is_draft=False, category=blog_category, lang="es"
    )

    with django_assert_num_queries(1):
        result = blog_entry_providers.get_blog_entry_by_slug(slug=blog_entry.slug)

    assert blog_entry.slug == slugify(blog_entry.title)

    fields = {"id", "content", "slug", "is_draft"}

    for field in fields:
        assert getattr(blog_entry, field) == getattr(result, field)
