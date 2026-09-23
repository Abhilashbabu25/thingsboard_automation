from playwright.sync_api import Page,expect, TimeoutError as PlaywrightTimeoutError

# Page class for interacting with the Dashboard
class DashboardPage:

    def __init__(self, page: Page):
        self.page = page
         # -------------------------
        # Dashboard Widget Locators
        # -------------------------

        self.temperature_locator = self.page.locator(
            "//div[contains(@class,'widget')][.//div[normalize-space()='Temperature']]//span[contains(@class,'widget-value')]"
        )

        self.humidity_locator = self.page.locator(
            "//div[contains(@class,'widget')][.//div[normalize-space()='Humidity']]//span[contains(@class,'widget-value')]"
        )

        self.power_locator = self.page.locator(
            "//div[contains(@class,'widget')][.//div[normalize-space()='Power Consumption']]//span[contains(@class,'widget-value')]"
        )

    def open_device_telemetry_dashboard(self):
        self.page.get_by_text(
            "Device Telemetry",
            exact=True
        ).click()

    def verify_widget_is_updating(
        self,
        widget_name,
        value_locator,
        # attempts=5,
        # interval=3,
        timeout=15000
    ):
        previous_value = value_locator.inner_text().strip()

        print(f"{widget_name} - Initial value: {previous_value}")
        
        try:
            expect(value_locator).not_to_have_text(
                previous_value,
                timeout=timeout
            )
            
            current_value = value_locator.inner_text().strip()
            
            print(
                f"{widget_name} updated:"
                f"{previous_value} -> {current_value}"
            )
            
            return True
        
        except PlaywrightTimeoutError:
            print(
                f"{widget_name} did not update"
                f"within {timeout/1000} seconds"
            )
            return False     

    def verify_all_widgets_are_updating(self):

        results = {
            "Temperature": self.verify_widget_is_updating(
                "Temperature",
                self.temperature_locator
            ),
            "Humidity": self.verify_widget_is_updating(
                "Humidity",
                self.humidity_locator
            ),
            "Power Consumption": self.verify_widget_is_updating(
                "Power Consumption",
                self.power_locator
            ),
        }

        return results

    def get_widget_value(self, value_locator):
        """
        Read the widget text and convert it to a float.
        Example:
        '25.5 °C' -> 25.5
        '65 %' -> 65.0
        """

        value_text = value_locator.inner_text().strip()

        # Extract the numeric part from the text
        numeric_value = float(value_text.split()[0])

        return numeric_value

    def get_telemetry_values(self):

        return {
            "Temperature": self.get_widget_value(self.temperature_locator),
            "Humidity": self.get_widget_value(self.humidity_locator),
            "Power Consumption": self.get_widget_value(self.power_locator),
        }