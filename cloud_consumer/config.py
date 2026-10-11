import os
from dotenv import load_dotenv

# Load variables from .env
load_dotenv()

EVENT_HUB_CONNECTION_STRING = os.getenv("EVENT_HUB_CONNECTION_STRING")

if not EVENT_HUB_CONNECTION_STRING:
    raise ValueError("Missing EVENT_HUB_CONNECTION_STRING in .env file!")