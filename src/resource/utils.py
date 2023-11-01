import os

import yaml
from fastapi import UploadFile, HTTPException
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from config import settings
from logger_config import logger
from src.resource.models import DeviceConfiguration
from src.resource.schemas import AppConfig


def create_device_configuration(db: Session, device_id: str, app_config: str, depth_config: str):
    try:
        device_config = DeviceConfiguration(device_id=device_id,
                                            app_config_uri=app_config,
                                            depth_config_uri=depth_config)
        db.add(device_config)
        db.commit()
    except IntegrityError as ex:
        db.rollback()
        logger.error(f"Device ID already exists. : {device_id}. Error: {str(ex)}")
        raise HTTPException(status_code=400, detail="Device ID already exists.")
    except Exception as ex:
        db.rollback()
        logger.error(f"Something went wrong. : {device_id}. Error: {str(ex)}")
        raise HTTPException(status_code=500, detail="Database error.")


def get_device_configuration(db: Session, device_id: str) -> DeviceConfiguration:
    return db.query(DeviceConfiguration).filter(DeviceConfiguration.device_id == device_id).first()


def save_file_to_static_folder(file: UploadFile, filename: str) -> str:
    file_path = os.path.join(settings.STATIC_DIR, filename)
    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())
    return file_path


def validate_app_config(file_content: str, device_id: int) -> AppConfig:
    try:
        parsed_content = yaml.safe_load(file_content)
        print(parsed_content)
        return AppConfig(**parsed_content)
    except yaml.YAMLError:
        raise HTTPException(status_code=400, detail="Invalid YAML content.")
    except ValidationError as e:
        logger.error(f"Error while creating configuration for device_id: {device_id}. Error: {str(e)}")
        raise HTTPException(status_code=400, detail=e.errors())
