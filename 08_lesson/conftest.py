import pytest
import os
import requests


@pytest.fixture(scope="session")
def auth_token():
    """Получает и кэширует токен авторизации на всю сессию."""
    try:
        from auth import get_auth_token
        token = get_auth_token()
        if not token:
            raise ValueError("Получен пустой токен авторизации")
        return token
    except Exception as e:
        raise RuntimeError(f"Не удалось получить токен авторизации: {e}")


@pytest.fixture
def api_client(auth_token):
    """Создаёт HTTP-клиент с авторизацией для тестов."""
    session = requests.Session()
    session.headers.update(auth_token)
    return session


@pytest.fixture
def base_url():
    """Возвращает базовый URL для API."""
    return os.getenv("YOUGILE_BASE_URL", "https://ru.yougile.com")