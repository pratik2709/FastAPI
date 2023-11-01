import os

from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.params import File, Depends
from sqlalchemy.orm import Session

from config import settings
from database import get_db
from src.resource.utils import save_file_to_static_folder, create_device_configuration

app = FastAPI()

load_dotenv()

def get_api_key(api_key_header: str = Depends(settings.api_key_header)):
    valid_api_keys = os.environ.get("VALID_API_KEYS", "").split(",")
    if api_key_header in valid_api_keys:
        return api_key_header
    raise HTTPException(status_code=400, detail="Invalid API key")


@app.get("/ping")
async def root():
    return {"message": "Hello World"}


@app.post("/device-configurations/{device_id}/")
async def create_configuration(device_id: str, app_config: UploadFile = File(...),
                               depth_config: UploadFile = File(...),
                               db: Session = Depends(get_db),
                               api_key: str = Depends(get_api_key)):
    try:
        app_config_path = save_file_to_static_folder(app_config, f"{device_id}_app_config.yaml")
        depth_config_path = save_file_to_static_folder(depth_config, f"{device_id}_depth.yaml")

        create_device_configuration(db, device_id, app_config_path, depth_config_path)
        return {"message": "Configuration created successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

