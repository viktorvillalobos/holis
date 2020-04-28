from factory.django import DjangoModelFactory
from apps.core import models


class AreaFactory(DjangoModelFactory):
    class Meta:
        model = models.Area

