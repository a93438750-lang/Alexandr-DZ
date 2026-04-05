from dotenv import load_dotenv
import os

load_dotenv()

BASE_URL = os.getenv("YOUGILE_BASE_URL")
print("DEBUG: BASE_URL =", BASE_URL)

if BASE_URL and BASE_URL.startswith("https://"):
    print("✅ OK: BASE_URL корректен")
else:
    print(f"❌ ERROR: BASE_URL содержит ошибку: {BASE_URL}")
