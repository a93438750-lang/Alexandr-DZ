import os
import requests
from dotenv import load_dotenv

load_dotenv()


def get_auth_token():
    """Возвращает заголовки для авторизации через API-ключ."""
    base_url = os.getenv("YOUGILE_BASE_URL")
    api_key = os.getenv("YOUGILE_API_KEY")
    if not base_url or not api_key:
        raise ValueError(
            "Не заданы YOUGILE_BASE_URL или YOUGILE_API_KEY"
        )
    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }