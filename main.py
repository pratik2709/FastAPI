import os

from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.params import File
from pydantic import BaseModel

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")


@app.get("/ping")
async def root():
    return {"message": "Hello World"}


def save_file_to_static_folder(file: UploadFile, filename: str) -> str:
    file_path = os.path.join(STATIC_DIR, filename)
    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())
    return file_path

class DeviceConfig(BaseModel):
    device_id: str


@app.post("/device-configurations/")
async def create_configuration(app_config: UploadFile = File(...),
                               depth_config: UploadFile = File(...)):
    try:
        # device_id = data.device_id
        app_config_path = save_file_to_static_folder(app_config, f"{1}_app_config.yaml")
        depth_config_path = save_file_to_static_folder(depth_config, f"{1}_depth.yaml")

        print("over here")
        print(app_config_path)
        print(depth_config_path)
        # create_device_configuration(device_id, app_config_path, depth_config_path)
        return {"message": "Configuration created successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
