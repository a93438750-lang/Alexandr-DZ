import os
import requests
from dotenv import load_dotenv

load_dotenv()

def get_auth_headers():
    base_url = os.getenv("YOUGILE_BASE_URL")
    api_key = os.getenv("YOUGILE_API_KEY")

    if not base_url or not api_key:
        raise ValueError("Не заданы YOUGILE_BASE_URL или YOUGILE_API_KEY в переменных окружения")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    return headers

def make_api_request(endpoint, method="GET", json_data=None):
    base_url = os.getenv("YOUGILE_BASE_URL")
    url = f"{base_url.rstrip('/')}/api-v2/{endpoint.lstrip('/')}"

    headers = get_auth_headers()

    response = requests.request(method=method, url=url, headers=headers, json=json_data)
    response.raise_for_status()

    try:
        return response.json()
    except ValueError:
        return {"status": "ok"}