import os
import requests
from requests.auth import HTTPBasicAuth

CELERY_FLOWER_USER = os.getenv("CELERY_FLOWER_USER")
CELERY_FLOWER_PASSWORD = os.getenv("CELERY_FLOWER_PASSWORD")

response = requests.get(
    "http://localhost:5555/api/workers",
    auth=HTTPBasicAuth(CELERY_FLOWER_USER, CELERY_FLOWER_PASSWORD),
)

assert response.status_code == 200
