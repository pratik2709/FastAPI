import os

from decouple import config

class Settings:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    STATIC_DIR = os.path.join(BASE_DIR, "static")
    # DATABASE_URL = config('DATABASE_URL')
    # STATIC_DIR_PATH = config('STATIC_DIR_PATH')

settings = Settings()
