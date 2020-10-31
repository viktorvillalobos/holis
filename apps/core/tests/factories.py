from factory.django import DjangoModelFactory

from apps.core import models


class CompanyFactory(DjangoModelFactory):
    name = "Adslab"

    class Meta:
        model = models.Company


class AreaFactory(DjangoModelFactory):
    class Meta:
        model = models.Area
