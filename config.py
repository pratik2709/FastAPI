import os

from fastapi.security import APIKeyHeader


class Settings:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    STATIC_DIR = os.path.join(BASE_DIR, "static")
    API_KEY_NAME = "X-API-KEY"
    api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

settings = Settings()
