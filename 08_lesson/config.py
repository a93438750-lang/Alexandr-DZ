from dotenv import load_dotenv
load_dotenv()

import os

BASE_URL = os.getenv("YOUGILE_BASE_URL", "https://ru.yougile.com")
AUTH_USERNAME = os.getenv("YOUGILE_USERNAME")
AUTH_PASSWORD = os.getenv("YOUGILE_PASSWORD")






