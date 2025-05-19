import os

from dotenv import load_dotenv

load_dotenv()

API_TOKEN = str(os.getenv("API_TOKEN"))
