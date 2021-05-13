import requests

response = requests.get(
    "http://localhost:5000/api/v1/healthcheck/", allow_redirects=False
)
assert response.status_code == 200
