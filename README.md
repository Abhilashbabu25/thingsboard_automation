# ThingsBoard Automation Project

This project contains automated UI and API tests for the ThingsBoard demo application.

## Project Scope

The project covers:
```

- UI Automation using Python, Pytest, and Playwright
- API Automation using Python, Pytest, and Requests
## Required tools

- Python 3.10 or later
- uv
- Visual Studio Code
- Test cases and bug reports in Excel

---
```bash

```
## Application Under Test


```bash
**ThingsBoard Demo:**
```

https://demo.thingsboard.io

1. Clone the repository:

  ```bash

  ```
## Test Coverage
2. Create and install dependencies:

  ```bash
### UI Automation
  ```

3. Install Playwright browsers:

  ```bash

  ```
Covered scenarios:
4. Configure environment variables by creating a `.env` file in the project root:
- Navigate to Dashboards
```text
- Open the Device Telemetry Dashboard
- Validate streaming data widgets are visible
- Validate widget labels such as:
  - Temperature
  - Humidity
  - Power Consumption
  ```
- Validate that telemetry values are updating
  ```env
- Capture screenshots as test evidence

### API Automation
  ```

The API automation validates ThingsBoard REST APIs.

Covered scenarios:
  ## UI tests

  ```bash
- Authenticate using:
  ```

  Run UI tests in headed mode:

  ```bash

  ```
- Obtain the JWT authentication token
  ## API tests

  ```bash
- Extract the Device ID
  ```
- Fetch telemetry data using:
  ## All tests

  ```bash
  `GET /api/plugins/telemetry/DEVICE/{deviceId}/values/timeseries`
  ```

- Validate API response status

  ## UI automation

  - Login to ThingsBoard
  - Navigate to the Device Telemetry Dashboard
  - Validate telemetry widgets are visible
  - Validate widget labels
  - Validate widgets are updating
  - Validate telemetry values are within an acceptable range
  - Capture screenshots as evidence

  ## API automation

  - Authenticate and obtain a JWT token
  - Fetch devices and extract the Device ID
  - Fetch device telemetry
  - Validate response structure
  - Validate telemetry fields and value types
  - Retry API requests when telemetry data is not available

  ## Test evidence
│       ├── pages/
  Screenshots generated during UI tests are stored in:
│       │   └── dashboard_page.py
  `evidence/ui/`

  ## Test documentation

  - Test cases: `test_data/test_cases.xlsx`
  - Bug reports: `test_data/bug_report.xlsx`

  ## Notes

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
│       └── screenshots
│
├── test_data/
│   ├── test_cases.xlsx
│   └── bug_report.xlsx
│
├── .env
├── pyproject.toml
├── uv.lock
└── README.md

# Prerequisites

## Make sure the following are installed:
Python 3.10 or later
uv
Visual Studio Code

Check Python installation:
python --version

Check uv installation:
uv --version

# Setup

1. Clone the Repository
git clone https://github.com/Abhilashbabu25/thingsboard_automation.git

2. Create and Install Dependencies
uv sync

3. Install Playwright Browsers
uv run playwright install

4. Configure Environment Variables
Create a .env file in the project root.

thingsboard-automation/
│
├── .env
├── pyproject.toml
├── README.md
└── src/

</>env
THINGSBOARD_URL=https://demo.thingsboard.io
THINGSBOARD_USERNAME=tenant@thingsboard.org
THINGSBOARD_PASSWORD=tenant


# Running Tests

Run UI Tests
uv run pytest src/thingsboard_automation/tests/ui -v

Run UI tests in headed mode:
uv run pytest src/thingsboard_automation/tests/ui -v --headed

Run API Tests
uv run pytest src/thingsboard_automation/tests/api -v

Run All Tests
uv run pytest src/thingsboard_automation/tests -v

# Test Coverage
UI Automation
Login to ThingsBoard
Navigate to Device Telemetry Dashboard
Validate telemetry widgets are visible
Validate widget labels
Validate widgets are updating
Validate telemetry values are within an acceptable range
Capture screenshots as evidence
API Automation
Authenticate and obtain JWT token
Fetch devices and extract Device ID
Fetch device telemetry
Validate response structure
Validate telemetry fields and value types
Retry API requests when telemetry data is not available
Test Evidence

# Screenshots generated during UI tests are stored in:

evidence/ui/
Test Documentation
Test cases: test_data/test_cases.xlsx
Bug reports: test_data/bug_report.xlsx
Notes
.env should not be committed to the repository.
Telemetry fields and ranges may vary depending on the selected device.
UI selectors may need updates if the ThingsBoard dashboard changes.