from djpaddle.models import Plan


def get_all_paddle_plans():
    return Plan.objects.all().prefetch_related("prices").distinct()
