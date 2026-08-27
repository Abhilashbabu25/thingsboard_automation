import requests
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

# Get telemetry data for a specific device
def test_get_telemetry_data():
    token = test_get_auth_token()
    devices = test_get_all_devices()
    print("Devices: ", devices)
    
    for index, device in enumerate(devices, start=1):
        device_id = device["id"]["id"]
        print(f"Fetching telemetry data for Device {index}: {device['name']} (ID: {device_id})")
    
    while True:
        try:
            selection = int(input("Enter the device number to fetch telemetry data for (0 to exit): "))
            if selection == 0:
                break
            elif 1 <= selection <= len(devices):
                device_id = devices[selection - 1]["id"]["id"]
            else:
                print("Invalid selection. Please try again.")
                continue
        except ValueError:
            print("Invalid input. Please enter a valid number.")
            continue

        headers = {
            "X-Authorization": f"Bearer {token}"
        }

        response = requests.get(
            f"{BASE_URL}/api/plugins/telemetry/DEVICE/{device_id}/values/timeseries",
            headers=headers,
            timeout=30,
        )

        assert response.status_code == 200

        data = response.json()

        assert isinstance(data, dict)
