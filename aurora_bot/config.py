import os
from dotenv import load_dotenv

load_dotenv()

def get_config():
    return {
        'TOKEN': os.getenv('TELEGRAM_BOT_TOKEN'),
        'WEATHER_TOKEN': os.getenv('WEATHER_API_TOKEN')
    }
