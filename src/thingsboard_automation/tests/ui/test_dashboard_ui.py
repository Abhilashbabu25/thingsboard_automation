import re
from playwright.sync_api import Page, expect
from thingsboard_automation.utils.config import Config
from pathlib import Path
from thingsboard_automation.pages.dashboard_page import DashboardPage
from thingsboard_automation.pages.login_page import LoginPage


# Test to verify the login functionality of the ThingsBoard application
def test_login_page(page: Page) -> None:
    page.goto(Config.THINGSBOARD_URL)
    page.get_by_role("textbox", name="Username (email)").click()
    page.get_by_role("textbox", name="Username (email)").fill(Config.THINGSBOARD_USERNAME)
    page.get_by_text("Password", exact=True).click()
    page.get_by_role("textbox", name="Password").fill(Config.THINGSBOARD_PASSWORD)
    page.get_by_role("button", name="Sign in").click()
    
    # Define both possible login errors
    invalid_credentials_error = page.get_by_text(
        "Invalid username or password",
        exact=True
    )

    inactive_account_error = page.get_by_text(
        "User account is not active",
        exact=True
    )

    # Wait briefly for either error message
    try:
        invalid_credentials_error.wait_for(
            state="visible",
            timeout=5000
        )

        login_error = "Invalid username or password"

    except:
        try:
            inactive_account_error.wait_for(
                state="visible",
                timeout=5000
            )

            login_error = "User account is not active"

        except:
            login_error = None

    # If any login error is found, capture screenshot
    if login_error:

        print(f"Login failed: {login_error}")

        # Create evidence/ui folder if it does not exist
        screenshot_dir = Path("src/thingsboard_automation/evidence/ui")
        screenshot_dir.mkdir(parents=True, exist_ok=True)

        # Capture login failure screenshot
        page.screenshot(path=str(screenshot_dir / "login_error.png"),
            full_page=True
        )

        # Fail the test
        assert False, f"Login failed: {login_error}"
        
    
# Test to verify that the dashboard page is loaded and the expected widgets are visible
def test_streaming_widgets_are_visible(page: Page):
    # Arrange - Open application and login
    login_page = LoginPage(page)
    login_page.open_and_login()

    # Create Dashboard Page object
    dashboard_page = DashboardPage(page)

    # Navigate to telemetry dashboard
    dashboard_page.open_device_telemetry_dashboard()
    
    expected_widgets = [
        "Temperature",
        "Humidity",
        "Power Consumption"
    ]

    for widget_name in expected_widgets:
        widget = page.get_by_text(widget_name, exact=True)
        expect(widget).to_be_visible()
        
# test to verify that the widgets on the dashboard are updating their values over time
def test_streaming_widgets_are_updating(page: Page):

    # Login again because this test gets a fresh page
    login_page = LoginPage(page)
    login_page.open_and_login()
    
    dashboard_page = DashboardPage(page)
    dashboard_page.open_device_telemetry_dashboard()
    # Login and navigate to the Device Telemetry Dashboard
    # dashboard_page.open_dashboard()

    results = dashboard_page.verify_all_widgets_are_updating()

    for widget_name, is_updating in results.items():

        assert is_updating, (
            f"{widget_name} is not updating within "
            f"the expected time"
        )
        
# Test to verify that the telemetry values displayed on the dashboard are within acceptable ranges
def test_telemetry_values_are_in_acceptable_range(page):

    # Login and navigate
    login_page = LoginPage(page)
    login_page.open_and_login()
    
    dashboard_page = DashboardPage(page)
    dashboard_page.open_device_telemetry_dashboard()
    
     # Get telemetry values
    values = dashboard_page.get_telemetry_values()

    screenshot_dir = Path("src/thingsboard_automation/evidence/ui")
    screenshot_dir.mkdir(parents=True, exist_ok=True)

    page.screenshot(
        path=str(screenshot_dir / "telemetry_values.png"),
        full_page=True
    )

    acceptable_ranges = {
        "Temperature": (0, 100),
        "Humidity": (0, 100),
        "Power Consumption": (0, 10000),
    }

    for widget_name, value in values.items():

        minimum, maximum = acceptable_ranges[widget_name]

        assert minimum <= value <= maximum, (
            f"{widget_name} value {value} is outside "
            f"the acceptable range {minimum} to {maximum}"
        )