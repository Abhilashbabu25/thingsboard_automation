import requests
import time
from thingsboard_automation.utils.config import Config

BASE_URL = Config.THINGSBOARD_URL
USERNAME = Config.THINGSBOARD_USERNAME
PASSWORD = Config.THINGSBOARD_PASSWORD

# Login to ThingsBoard and get the authentication token
def test_get_auth_token():
    
     headers = {
            "Content-Type": f"application/json"
        }
     response = requests.post(
        f"{BASE_URL}/api/auth/login",
        headers=headers,
        json={
            "username": USERNAME,
            "password": PASSWORD
        },
        timeout=30,
    )

     assert response.status_code == 200

     data = response.json()

     assert "token" in data

     return data["token"]
 
# Get all devices for the tenant
def test_get_all_devices():
    token = test_get_auth_token()

    headers = {
        "X-Authorization": f"Bearer {token}"
    }

    devices_response = requests.get(
        f"{BASE_URL}/api/tenant/devices",
        headers=headers,
        params= {
                    "pageSize": 10,
                    "page": 0
                },
        
            )
    devices_response.raise_for_status()
    assert devices_response.status_code == 200

    devices = devices_response.json()["data"]
    
    for device in devices:
        print("Device Name: ", device["name"])
        print("Device ID: ", device["id"]["id"])
        print("Device Type: ", device["type"])
        print("Device Label: ", device["label"])
        print("Device Created Time: ", device["createdTime"])
        print("Device Additional Info: ", device.get("additionalInfo", {}))
        print("-----------------------------")
    return devices

# Get telemetry data for a specific device with retry mechanism
def get_telemetry_with_retry(
    token,
    device_id,
    max_attempts=5,
    interval=3
):

    headers = {
        "X-Authorization": f"Bearer {token}"
    }

    for attempt in range(1, max_attempts + 1):

        response = requests.get(
            f"{BASE_URL}/api/plugins/telemetry/DEVICE/{device_id}/values/timeseries",
            headers=headers,
            timeout=30,
        )

        assert response.status_code == 200

        data = response.json()

        if data:
            print(
                f"Telemetry data received "
                f"on attempt {attempt}"
            )
            return data

        print(
            f"No telemetry data. "
            f"Retry {attempt}/{max_attempts}"
        )

        time.sleep(interval)

    raise AssertionError(
        f"No telemetry data received after "
        f"{max_attempts} attempts"
    )


def test_get_telemetry_data():

    # Step 1: Authenticate
    token = test_get_auth_token()

    # Step 2: Get devices
    devices = test_get_all_devices()

    assert len(devices) > 0, "No devices found"

    # Step 3: Select a device
    device = devices[0]

    device_id = device["id"]["id"]

    print(
        f"Selected Device: {device['name']} "
        f"(ID: {device_id})"
    )

    # Step 4: Get telemetry with retry
    telemetry_data = get_telemetry_with_retry(
        token,
        device_id
    )

    # Step 5: Validate response structure
    assert isinstance(telemetry_data, dict)
    assert len(telemetry_data) > 0

    print("Available telemetry fields:")
    print(list(telemetry_data.keys()))

    # Step 6: Validate available telemetry fields
    fields_to_validate = list(telemetry_data.keys())[:5]

    assert len(fields_to_validate) >= 3, (
        "Less than 3 telemetry fields are available"
    )

    for field in fields_to_validate:

        values = telemetry_data[field]

        assert isinstance(values, list), (
            f"{field} should contain a list"
        )

        assert len(values) > 0, (
            f"{field} contains no telemetry values"
        )

        latest_value = values[-1]

        assert "ts" in latest_value, (
            f"Timestamp missing for {field}"
        )

        assert "value" in latest_value, (
            f"Value missing for {field}"
        )

        assert isinstance(latest_value["ts"], int), (
            f"Timestamp should be an integer for {field}"
        )

        # Validate numeric value where applicable
        try:
            float(latest_value["value"])
        except (ValueError, TypeError):
            raise AssertionError(
                f"{field} value is not numeric: "
                f"{latest_value['value']}"
            )

        print(
            f"{field}: "
            f"Timestamp={latest_value['ts']}, "
            f"Value={latest_value['value']}"
        )


