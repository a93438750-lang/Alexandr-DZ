import os
import requests
from dotenv import load_dotenv

load_dotenv()


def get_company_id():
    """Получает ID компании."""
    base_url = os.getenv("YOUGILE_BASE_URL")
    login = os.getenv("YOUGILE_USERNAME")
    password = os.getenv("YOUGILE_PASSWORD")
    url = f"{base_url.rstrip('/')}/api-v2/auth/companies"
    response = requests.post(
        url,
        json={"login": login, "password": password},
        headers={"Content-Type": "application/json"},
    )
    response.raise_for_status()
    data = response.json()
    return data["content"][0]["id"] if data.get("content") else None


def get_api_keys():
    """Получает список API-ключей."""
    base_url = os.getenv("YOUGILE_BASE_URL")
    login = os.getenv("YOUGILE_USERNAME")
    password = os.getenv("YOUGILE_PASSWORD")
    
    company_id = get_company_id()
    if not company_id:
        raise ValueError("ID компании не получен")
        
    url = f"{base_url.rstrip('/')}/api-v2/auth/keys/get"
    response = requests.post(
        url,
        json={"login": login, "password": password, "companyId": company_id},
        headers={"Content-Type": "application/json"},
    )
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    try:
        keys = get_api_keys()
        print("Список ключей:", keys)
    except Exception as e:
        print("Ошибка:", e)