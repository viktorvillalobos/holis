from django.template.defaultfilters import slugify

import pytest
from model_bakery import baker

from ...providers import page as page_providers


@pytest.mark.django_db
def test_get_page_by_slug(django_assert_num_queries):
    page = baker.make("web.Page", is_draft=False)

    with django_assert_num_queries(1):
        result = page_providers.get_page_by_slug(slug=page.slug)

    assert page.slug == slugify(page.title)

    fields = {"id", "content", "slug", "is_draft"}

    for field in fields:
        assert getattr(page, field) == getattr(result, field)
