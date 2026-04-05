import pytest
import requests
from auth import get_auth_token
from config import BASE_URL



@pytest.fixture(scope="session")
def base_url():
    """Предоставляет базовый URL API."""
    return BASE_URL



@pytest.fixture(scope="session")
def auth_token():
    """Получает и кэширует токен авторизации на всю сессию."""
    try:
        token = get_auth_token()
        if not token:
            raise ValueError("Получен пустой токен авторизации")
        return token
    except Exception as e:
        raise RuntimeError(f"Не удалось получить токен авторизации: {e}")



@pytest.fixture
def api_client(auth_token):
    """Создаёт HTTP‑клиент с авторизацией для тестов."""
    session = requests.Session()
    session.headers.update({
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/json"
    })
    session.timeout = 10  # Таймаут 10 секунд
    return session




