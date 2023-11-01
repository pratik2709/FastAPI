import os
from io import BytesIO

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

    app_config_content = b"app_config_content_here"
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

