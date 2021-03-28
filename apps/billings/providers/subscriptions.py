from django.conf import settings

import requests

from .. import paddle_endpoints


def get_total_current_full_plan_subscriptions() -> int:
    payload = {
        "vendor_id": settings.DJPADDLE_VENDOR_ID,
        "vendor_auth_code": settings.DJPADDLE_API_KEY,
        "plan_id": "648396",
    }

    response = requests.post(paddle_endpoints.SUBCSCRIPTION_USERS, payload)

    return len(response.json()["response"])
