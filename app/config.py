import os
from dotenv import load_dotenv

load_dotenv()

def get(key: str, default: str = "") -> str:
    return os.getenv(key, default)

OPENAI_API_KEY = get("OPENAI_API_KEY")
OPENAI_BASE_URL = get("OPENAI_BASE_URL", "https://api.deepseek.com")
BOCHA_API_KEY = get("BOCHA_API_KEY")
SERVERCHAN_KEY = get("SERVERCHAN_KEY")
MODEL = "deepseek-chat"