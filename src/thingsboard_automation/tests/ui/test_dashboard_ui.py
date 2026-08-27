import re
from playwright.sync_api import Page, expect
from thingsboard_automation.utils.config import Config


def test_login_page(page: Page) -> None:
    page.goto(Config.THINGSBOARD_URL)
    page.get_by_role("textbox", name="Username (email)").click()
    print("Username: ", Config.THINGSBOARD_USERNAME)
    page.get_by_role("textbox", name="Username (email)").fill(Config.THINGSBOARD_USERNAME)
    print("Password: ", Config.THINGSBOARD_PASSWORD)
    page.get_by_text("Password", exact=True).click()
    page.get_by_role("textbox", name="Password").fill(Config.THINGSBOARD_PASSWORD)
    page.get_by_role("button", name="Sign in").click()