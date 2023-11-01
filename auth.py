import os

from fastapi import HTTPException
from fastapi.params import Depends

from config import settings


def get_api_key(api_key_header: str = Depends(settings.api_key_header)):
    valid_api_keys = os.environ.get("VALID_API_KEYS", "").split(",")
    if api_key_header in valid_api_keys:
        return api_key_header
    raise HTTPException(status_code=400, detail="Invalid API key")
