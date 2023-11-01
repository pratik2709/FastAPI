import uuid

import pytest
import yaml
from fastapi import HTTPException

from src.resource.utils import validate_app_config


def test_validate_app_config_valid():
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
    result = validate_app_config(app_config_content, 1)
    assert result is not None


def test_validate_app_config_invalid_yaml():
    invalid_content  = {
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
        }
    }
    content = yaml.dump(invalid_content).encode('utf-8')
    with pytest.raises(HTTPException) as exc_info:
        validate_app_config(content, 1)
    assert exc_info.value.status_code == 400
    assert "Invalid YAML content. Missing or improper fields" in str(exc_info.value.detail)
