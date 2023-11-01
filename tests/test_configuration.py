import json
import os
from io import BytesIO

import yaml
from fastapi.testclient import TestClient

from main import app
import uuid


client = TestClient(app)


def test_read_main():
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


# TODO: create a pytest fixture which creates a test DB runs the migrations
#  and cleans up after test finishes
def test_create_configuration():
    device_id = str(uuid.uuid4())

    app_config_content = {
        "alive_poll_time": 1,
        "depth": {
            "tolerance_m": 2.5,
            "deck_length": {
                "max": 16,
                "default": 14
            }
        },
        "device": {
            "id": str(uuid.uuid4()),
            "type": "PC"
        },
        "networking": {
            "orchestrator_connect_ip": "tcp://localhost:5555",
            "orchestrator_heartbeat_timeout": 5,
            "power_service_connect_ip": "tcp://localhost:5556",
            "power_service_heartbeat_timeout": 5,
            "zmq_router_bind_ip": "tcp://*:5555"
        },
        "file_saving": {
            "cache_previous_frame": 125,
            "delete_video": True,
            "fps": 25,
            "inference_name": "infer",
            "max_event_duration_sec": 300,
            "min_event_duration_sec": 3,
            "post_threshold_sec": 20,
            "ppe_event_ratio": 0.3,
            "saved_directory": "output/events",
            "video_name": "out",
            "codec": "mp4v",
            "resolution": {
                "height": 720,
                "width": 1280
            }
        },
        "gps": {
            "enable": True,
            "poll_time": 5
        },
        "upload": {
            "enable": True,
            "trigger_time_sec": 30
        },
        "device_setup": {
            "truck": False
        },
        "video_sources": {
            0: "file:///videos/warehouse_testing/Positive/cnt-enx-01/f32b131a-e5c5-4217-b707-889c1f2efee5_Isle-DK-enx1_ARDC_-_Isle_complete.mp4"
        },
        "camera_ids": {
            0: str(uuid.uuid4()),
            1: str(uuid.uuid4())
        }
    }

    app_config_content = yaml.dump(app_config_content).encode('utf-8')
    depth_config_content = b"depth_config_content_here"

    app_config_file = BytesIO(app_config_content)
    depth_config_file = BytesIO(depth_config_content)

    headers = {
        "X-API-KEY": "key1"
    }

    response = client.post(
        f"/device-configurations/{device_id}/",
        headers=headers,
        files={
            "app_config": ("test_app_config.yaml", app_config_file),
            "depth_config": ("test_depth_config.yaml", depth_config_file)
        }
    )

    assert response.status_code == 200
    assert response.json() == {"message": "Configuration created successfully"}

    response = client.get(f"/device-configurations/{device_id}/", headers=headers)
    assert response.status_code == 200
    assert "app_config_path" in response.json()
    assert "depth_config_path" in response.json()

    os.remove('static/' + str(device_id + '_app_config.yaml'))
    os.remove('static/' + str(device_id + '_depth.yaml'))

