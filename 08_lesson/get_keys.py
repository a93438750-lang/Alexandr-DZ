import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

def get_company_id():
    """
    Получает ID компании через API YouGile.
    Правильно обрабатывает структуру ответа сервера.
    """
    base_url = os.getenv("YOUGILE_BASE_URL")
    username = os.getenv("YOUGILE_USERNAME")
    password = os.getenv("YOUGILE_PASSWORD")

    if not all([base_url, username, password]):
        raise ValueError(
            "Не заданы YOUGILE_BASE_URL, YOUGILE_USERNAME или YOUGILE_PASSWORD"
        )

    url = f"{base_url.rstrip('/')}/api-v2/auth/companies"
    try:
        response = requests.post(
            url,
            json={"login": username, "password": password},
            headers={"Content-Type": "application/json"},
        )
        print(f"[DEBUG] Ответ компаний: Статус {response.status_code}, Текст: {response.text}")
        response.raise_for_status()
        
        data = response.json()
        # Данные о компаниях находятся внутри ключа "content"
        companies = data.get("content", [])
        if companies:
            return companies[0]["id"]
        else:
            print("[DEBUG] Ошибка: Список компаний в ответе пуст.")
            return None

    except Exception as e:
        print(f"[DEBUG] Ошибка при получении ID компании: {e}")
        raise

def get_api_keys():
    """
    Получает список API-ключей для компании.
    """
    base_url = os.getenv("YOUGILE_BASE_URL")
    username = os.getenv("YOUGILE_USERNAME")
    password = os.getenv("YOUGILE_PASSWORD")

    if not all([base_url, username, password]):
        raise ValueError(
            "Не заданы YOUGILE_BASE_URL, YOUGILE_USERNAME или YOUGILE_PASSWORD"
        )

    try:
        company_id = get_company_id()
        if not company_id:
            raise ValueError("Не удалось получить ID компании")

        url = f"{base_url.rstrip('/')}/api-v2/auth/keys/get"
        print(f"[DEBUG] Запрашиваем ключи по URL: {url}")
        
        response = requests.post(
            url,
            json={
                "login": username,
                "password": password,
                "companyId": company_id,
            },
            headers={"Content-Type": "application/json"},
        )
        
        print(f"[DEBUG] Ответ ключей: Статус {response.status_code}")
        
        # Проверяем, успешен ли запрос, прежде чем парсить JSON
        if response.status_code == 200:
            json_resp = response.json()
            print(f"[DEBUG] JSON ответа: {json_resp}")
            return json_resp
        else:
            # Если статус не 200, выводим текст ошибки
            print(f"[DEBUG] Ошибка сервера. Текст ответа: {response.text}")
            response.raise_for_status() # Вызовет исключение для общего обработчика

    except Exception as e:
        print(f"Ошибка: {e}")
        raise

if __name__ == "__main__":
    try:
        keys = get_api_keys()
        if keys:
            print("\nУспешно получен список API-ключей:")
            for key in keys:
                # --- ИСПРАВЛЕННАЯ СТРОКА ---
                # Используем key.get('key'), так как именно так поле называется в JSON от сервера
                status = "Удален" if key.get("удалено") else "Активен"
                print(f" - Ключ: {key.get('key')}. Статус: {status}")
        else:
            print("Список ключей пуст или не был получен.")
            
    except Exception as e:
        print(f"\n⛔️ Произошла ошибка при выполнении скрипта: {e}")