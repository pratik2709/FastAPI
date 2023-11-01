from typing import Dict
from uuid import UUID

from pydantic import BaseModel, validator


class Device(BaseModel):
    id: str
    type: str

    @validator("id", pre=True)
    def validate_uuid(cls, value):
        try:
            UUID(value, version=4)
            return value
        except ValueError:
            raise ValueError("Invalid UUID format")


class Networking(BaseModel):
    orchestrator_connect_ip: str
    orchestrator_heartbeat_timeout: int
    power_service_connect_ip: str
    power_service_heartbeat_timeout: int
    zmq_router_bind_ip: str

class FileSaving(BaseModel):
    cache_previous_frame: int
    delete_video: bool
    fps: int
    inference_name: str
    max_event_duration_sec: int
    min_event_duration_sec: int
    post_threshold_sec: int
    ppe_event_ratio: float
    saved_directory: str
    video_name: str
    codec: str
    resolution: Dict[str, int]

class GPS(BaseModel):
    enable: bool
    poll_time: int

class Upload(BaseModel):
    enable: bool
    trigger_time_sec: int

class DeviceSetup(BaseModel):
    truck: bool

class Depth(BaseModel):
    tolerance_m: float
    deck_length: Dict[str, int]

class AppConfig(BaseModel):
    alive_poll_time: int
    depth: Depth
    device: Device
    networking: Networking
    file_saving: FileSaving
    gps: GPS
    upload: Upload
    device_setup: DeviceSetup
    video_sources: Dict[int, str]
    camera_ids: Dict[int, str]

