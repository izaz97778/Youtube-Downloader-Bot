import os

# Read environment variables
BOT_TOKEN = os.environ.get("BOT_TOKEN")
APP_ID = os.environ.get("API_ID")
API_HASH = os.environ.get("API_HASH")

# Check if any are missing
if not all([BOT_TOKEN, APP_ID, API_HASH]):
    raise ValueError("Missing required environment variables: BOT_TOKEN, API_ID, or API_HASH")

# Convert APP_ID to integer
APP_ID = int(APP_ID)

# Other configuration
youtube_next_fetch = 0  # time in minutes
EDIT_TIME = 5
