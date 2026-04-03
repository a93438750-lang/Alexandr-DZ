import pytest
from auth import get_auth_token
from config import BASE_URL, AUTH_CREDENTIALS

@pytest.fixture(scope="session")
def base_url():
    return BASE_URL

@pytest.fixture(scope="session")
def auth_token():
    token = get_auth_token()
    return token


@pytest.fixture
def api_client(auth_token):
    
    session = requests.Session()
    session.headers.update({
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/json"
    })
    return session
