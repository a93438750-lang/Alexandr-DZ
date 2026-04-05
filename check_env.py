from dotenv import load_dotenv
import os

load_dotenv()

BASE_URL = os.getenv("YOUGILE_BASE_URL")
AUTH_USERNAME = os.getenv("YOUGILE_USERNAME")
AUTH_PASSWORD = os.getenv("YOUGILE_PASSWORD")

print("DEBUG: BASE_URL =", BASE_URL)
print("DEBUG: AUTH_USERNAME =", AUTH_USERNAME)
print("DEBUG: AUTH_PASSWORD =", AUTH_PASSWORD)

if BASE_URL and BASE_URL.startswith("https://"):
    print("✅ OK: BASE_URL корректен")
else:
    print(f"❌ ERROR: BASE_URL содержит ошибку: {BASE_URL}")
