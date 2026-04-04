import requests
from config import AUTH_USERNAME, AUTH_PASSWORD, BASE_URL



def get_auth_token():
    
    if not AUTH_USERNAME or not AUTH_PASSWORD:
        raise ValueError(
            "Не заданы YOUGILE_USERNAME или YOUGILE_PASSWORD в переменных окружения"
        )

    auth_url = f"{BASE_URL}/api-v2/auth/login"
    payload = {
        "username": AUTH_USERNAME,
        "password": AUTH_PASSWORD
    }

    try:
        response = requests.post(auth_url, json=payload)
        response.raise_for_status()

        response_data = response.json()
        token = response_data.get("token")

        if not token:
            raise ValueError("Сервер не вернул токен авторизации. Проверьте учётные данные.")

        return token

    except requests.exceptions.RequestException as e:
        print(f"Ошибка сети или недоступность сервера: {e}")
        raise
    except ValueError as e:
        print(f"Ошибка парсинга ответа сервера: {e}")
        raise



