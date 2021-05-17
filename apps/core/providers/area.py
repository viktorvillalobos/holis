from apps.core.models import Area


def get_area_instance_by_id(area_id: int) -> Area:
    return Area.objects.get(id=area_id)


def get_company_areas_by_company_id(company_id: int) -> list[Area]:
    return Area.objects.filter(company_id=company_id)
