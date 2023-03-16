# Description: Configuration file for Ponzu
import os
from dotenv import load_dotenv

load_dotenv()

SLACK_APP_TOKEN = os.getenv("SLACK_APP_TOKEN")
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SLACK_SIGNING_SECRET = os.getenv("SLACK_SIGNING_SECRET")
