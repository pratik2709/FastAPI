import logging
import azure.functions as func
import requests  # Ensure you have this installed

DEVICE_CONFIG_SERVICE_URL = "http://127.0.0.1:5000/device-configurations/"

def main(event: func.EventGridEvent):
    result = f"Event ID: {event.id} \n Event Type: {event.event_type} \n Data: {event.get_json()}"

    logging.info(f"Python EventGrid trigger processed an event: {result}")

    device_id = event.get_json().get("device_id")
    if not device_id:
        return func.HttpResponse("No device_id found in Event Grid data", status_code=400)

    # Fetch the configuration for the given device_id
    response = requests.get(f"{DEVICE_CONFIG_SERVICE_URL}{device_id}/")

    if response.status_code != 200:
        return func.HttpResponse(f"Failed to fetch configuration for device {device_id}", status_code=500)

    return func.HttpResponse(response.json(), status_code=200)
