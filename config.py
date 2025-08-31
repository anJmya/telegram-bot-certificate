import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
ADMIN_ID = int(os.getenv('ADMIN_ID'))
GOOGLE_CREDS = os.getenv('GOOGLE_CREDS')
SOURCE_SHEET_ID = os.getenv('SOURCE_SHEET_ID')
TARGET_SHEET_ID = os.getenv('TARGET_SHEET_ID')
