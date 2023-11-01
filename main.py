from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.params import File, Depends
from sqlalchemy.orm import Session

from auth import get_api_key
from database import get_db
from logger_config import logger
from src.resource.utils import save_file_to_static_folder, create_device_configuration, get_device_configuration, \
    validate_app_config

app = FastAPI()

load_dotenv()


@app.get("/ping")
async def root():
    return {"message": "Hello World"}


@app.post("/device-configurations/{device_id}/")
async def create_configuration(device_id: str, app_config: UploadFile = File(...),
                               depth_config: UploadFile = File(...),
                               db: Session = Depends(get_db),
                               api_key: str = Depends(get_api_key)):
    logger.info(f"Received request to create configuration for device_id: {device_id}")
    try:
        # todo: use a generator function to save memory
        app_config_content = await app_config.read()
        validate_app_config(app_config_content.decode(), device_id)
        app_config_path = save_file_to_static_folder(app_config, f"{device_id}_app_config.yaml")
        depth_config_path = save_file_to_static_folder(depth_config, f"{device_id}_depth.yaml")
        create_device_configuration(db, device_id, app_config_path, depth_config_path)
        return {"message": "Configuration created successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/device-configurations/{device_id}/")
async def get_configuration(device_id: str, db: Session = Depends(get_db), api_key: str = Depends(get_api_key)):
    try:
        device_config = get_device_configuration(db, device_id)
        if not device_config:
            raise HTTPException(status_code=404, detail="Configuration not found")
        return {
            "app_config_path": device_config.app_config_uri,
            "depth_config_path": device_config.depth_config_uri
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
