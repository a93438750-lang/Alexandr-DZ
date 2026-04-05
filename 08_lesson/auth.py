from python_dotenv import load_dotenv
import os
import requests

load_dotenv()

def get_auth_token():
    BASE_URL = os.getenv("YOUGILE_BASE_URL")
    AUTH_USERNAME = os.getenv("YOUGILE_USERNAME")
    AUTH_PASSWORD = os.getenv("YOUGILE_PASSWORD")

    if not BASE_URL or not AUTH_USERNAME or not AUTH_PASSWORD:
        raise ValueError("Не заданы YOUGILE_BASE_URL, YOUGILE_USERNAME или YOUGILE_PASSWORD в переменных окружения")

    auth_url = f"{BASE_URL.rstrip('/')}/api/v2/auth/login"  # ИЗМЕНЕННЫЙ URL

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    response = requests.post(
        auth_url,
        json={
            "email": AUTH_USERNAME,
            "password": AUTH_PASSWORD
        },
        headers=headers
    )

    response.raise_for_status()
    return response.json().get("token")
