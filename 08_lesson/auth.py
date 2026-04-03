import requests
from config import AUTH_USERNAME, AUTH_PASSWORD, BASE_URL

def get_auth_token():
    
    if not AUTH_USERNAME or not AUTH_PASSWORD:
        raise ValueError(
            
        )

    auth_url = f"{BASE_URL}/api-v2/auth/login"
    payload = {"username": AUTH_USERNAME, "password": AUTH_PASSWORD}
    response = requests.post(auth_url, json=payload)
    response.raise_for_status()
    return response.json().get("token")

