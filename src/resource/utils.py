import os

from fastapi import UploadFile
from sqlalchemy.orm import Session

from config import settings
from src.resource.models import DeviceConfiguration


def create_device_configuration(db: Session, device_id: str, app_config: str, depth_config: str):
    device_config = DeviceConfiguration(device_id=device_id,
                                        app_config_uri=app_config,
                                        depth_config_uri=depth_config)
    db.add(device_config)
    db.commit()


def get_device_configuration(db: Session, device_id: str) -> DeviceConfiguration:
    return db.query(DeviceConfiguration).filter(DeviceConfiguration.device_id == device_id).first()


def save_file_to_static_folder(file: UploadFile, filename: str) -> str:
    file_path = os.path.join(settings.STATIC_DIR, filename)
    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())
    return file_path
