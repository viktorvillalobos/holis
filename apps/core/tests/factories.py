from apps.core import models
from factory.django import DjangoModelFactory


class CompanyFactory(DjangoModelFactory):
    name = "Adslab"

    class Meta:
        model = models.Company


class AreaFactory(DjangoModelFactory):
    class Meta:
        model = models.Area
