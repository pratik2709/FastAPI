import os

from fastapi import UploadFile

from main import STATIC_DIR
from src.resource.models import DeviceConfiguration


# def create_device_configuration(device_id: str, app_config: str, depth_config: str):
#     device_config = DeviceConfiguration(device_id=device_id, app_config=app_config, depth_config=depth_config)
#     session.add(device_config)
#     session.commit()
#     session.close()

def save_file_to_static_folder(file: UploadFile, filename: str) -> str:
    file_path = os.path.join(STATIC_DIR, filename)
    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())
    return file_path
