# ThingsBoard Automation Project

This project contains automated **UI and API tests** for the ThingsBoard Demo application.

The project includes:

- UI Automation using Python, Pytest, and Playwright
- API Automation using Python, Pytest, and Requests
- Test cases and bug reports in Excel
- Screenshot evidence for UI test execution

---

## Application Under Test

**ThingsBoard Demo:**  
https://demo.thingsboard.io

---

## Project Structure

```text
thingsboard-automation/
│
├── src/
│   └── thingsboard_automation/
│       │
│       ├── pages/
│       │   ├── login_page.py
│       │   └── dashboard_page.py
│       │
│       ├── tests/
│       │   ├── ui/
│       │   │   └── test_dashboard_ui.py
│       │   │
│       │   └── api/
│       │       └── test_api_telemetry.py
│       │
│       ├── utils/
│       │   └── config.py
│       │
│       └── main.py
│
├── evidence/
│   └── ui/
│       └── screenshots/
│
├── test_data/
│   ├── test_cases.xlsx
│   └── bug_report.xlsx
│
├── .env
├── pyproject.toml
├── uv.lock
└── README.md
```

---

## Prerequisites

Make sure the following are installed:

- Python 3.10 or later
- uv
- Visual Studio Code

### Check Python Installation

```bash
python --version
```

### Check uv Installation

```bash
uv --version
```

---

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Abhilashbabu25/thingsboard_automation.git
```

Navigate to the project directory:

```bash
cd thingsboard_automation
```

### 2. Install Dependencies

```bash
uv sync
```

### 3. Install Playwright Browsers

```bash
uv run playwright install
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```text
thingsboard-automation/
├── .env
├── pyproject.toml
├── README.md
└── src/
```

Add the following values to the `.env` file:

```env
THINGSBOARD_URL=https://demo.thingsboard.io
THINGSBOARD_USERNAME=tenant@thingsboard.org
THINGSBOARD_PASSWORD=tenant
```

---

## Running Tests

### Run UI Tests

```bash
uv run pytest src/thingsboard_automation/tests/ui -v
```

### Run UI Tests in Headed Mode

```bash
uv run pytest src/thingsboard_automation/tests/ui -v --headed
```

### Run API Tests

```bash
uv run pytest src/thingsboard_automation/tests/api -v
```

### Run All Tests

```bash
uv run pytest src/thingsboard_automation/tests -v
```

---

## Test Coverage

### UI Automation

The UI automation covers the following scenarios:

- Login to ThingsBoard
- Navigate to the Device Telemetry Dashboard
- Validate streaming data widgets are visible
- Validate widget labels:
  - Temperature
  - Humidity
  - Power Consumption
- Validate that telemetry widgets are updating
- Validate telemetry values are within an acceptable range
- Capture screenshots as test evidence

### API Automation

The API automation covers the following scenarios:

- Authenticate using `POST /api/auth/login`
- Obtain a JWT authentication token
- Fetch available devices
- Extract the Device ID
- Fetch telemetry using:

```text
GET /api/plugins/telemetry/DEVICE/{deviceId}/values/timeseries
```

- Validate API response status
- Validate response structure
- Validate 3–5 telemetry fields
- Validate telemetry value types
- Retry API requests when telemetry data is not immediately available

---

## Test Evidence

Screenshots generated during UI test execution are stored in:

```text
evidence/ui/
```

---

## Test Documentation

The project includes the following test documentation:

- **Test Cases:** `test_data/test_cases.xlsx`
- **Bug Reports:** `test_data/bug_report.xlsx`

---

## Technologies Used

- Python
- Pytest
- Playwright
- Requests
- python-dotenv
- uv

---

## Notes

- Do not commit the `.env` file to a public repository.
- Telemetry fields and acceptable ranges may vary depending on the selected device.
- UI selectors may need to be updated if the ThingsBoard dashboard UI changes.
- Screenshots are generated during UI test execution.