from typing import Any

from django.db import models


class LowerCharField(models.CharField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_prep_value(self, value):
        return str(value).lower()

    def to_python(self, value: Any) -> Any:
        return super().to_python(value).lower()
