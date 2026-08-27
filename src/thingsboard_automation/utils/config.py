import os

from dotenv import load_dotenv

load_dotenv()

class Config:
    THINGSBOARD_URL = os.getenv("THINGSBOARD_URL")
    THINGSBOARD_USERNAME = os.getenv("THINGSBOARD_USERNAME")
    THINGSBOARD_PASSWORD = os.getenv("THINGSBOARD_PASSWORD")