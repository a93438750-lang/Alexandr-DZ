import pytest
import requests
from auth import get_auth_token
from config import BASE_URL



@pytest.fixture(scope="session")
def base_url():
    return BASE_URL



@pytest.fixture(scope="session")
def auth_token():
    try:
        token = get_auth_token()
        if not token:
            raise ValueError(
               
            )
        return token
    except Exception as e:
        raise RuntimeError(f"Не удалось получить токен авторизации: {e}")



@pytest.fixture
def api_client(auth_token):
    session = requests.Session()
    session.headers.update({
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/json"
    })
    session.timeout = 10  # Таймаут 10 секунд
    return session



