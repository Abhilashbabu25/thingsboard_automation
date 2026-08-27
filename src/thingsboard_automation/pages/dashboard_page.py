import time

from playwright.sync_api import Page


class DashboardPage:

    def __init__(self, page: Page):
        self.page = page

    def verify_widget_is_updating(
        self,
        widget_name,
        value_locator,
        attempts=5,
        interval=3
    ):
        previous_value = value_locator.inner_text()

        print(f"{widget_name} - Initial value: {previous_value}")

        for attempt in range(1, attempts + 1):

            time.sleep(interval)

            current_value = value_locator.inner_text()

            print(
                f"{widget_name} - Attempt {attempt}: "
                f"{current_value}"
            )

            if current_value != previous_value:
                return True

        return False

    def verify_all_widgets_are_updating(self):

        temperature_locator = self.page.locator(
            "YOUR_TEMPERATURE_VALUE_SELECTOR"
        )

        humidity_locator = self.page.locator(
            "YOUR_HUMIDITY_VALUE_SELECTOR"
        )

        power_locator = self.page.locator(
            "YOUR_POWER_VALUE_SELECTOR"
        )

        results = {
            "Temperature": self.verify_widget_is_updating(
                "Temperature",
                temperature_locator
            ),
            "Humidity": self.verify_widget_is_updating(
                "Humidity",
                humidity_locator
            ),
            "Power Consumption": self.verify_widget_is_updating(
                "Power Consumption",
                power_locator
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

        temperature_locator = self.page.locator(
            "YOUR_TEMPERATURE_VALUE_SELECTOR"
        )

        humidity_locator = self.page.locator(
            "YOUR_HUMIDITY_VALUE_SELECTOR"
        )

        power_locator = self.page.locator(
            "YOUR_POWER_VALUE_SELECTOR"
        )

        return {
            "Temperature": self.get_widget_value(temperature_locator),
            "Humidity": self.get_widget_value(humidity_locator),
            "Power Consumption": self.get_widget_value(power_locator),
        }