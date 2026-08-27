from playwright.sync_api import Page

from thingsboard_automation.utils.config import Config

class LoginPage:

    def __init__(self, page: Page):
        self.page = page

    def open(self):
        self.page.goto(Config.THINGSBOARD_URL)

    def login(self):
        self.page.get_by_role("textbox",name="Username (email)").fill(Config.THINGSBOARD_USERNAME)
        self.page.get_by_role("textbox",name="Password").fill(Config.THINGSBOARD_PASSWORD)
        self.page.get_by_role("button",name="Sign in").click()
        
    def open_and_login(self):
        self.open()
        self.login()