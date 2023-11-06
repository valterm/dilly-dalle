import os
import logging

TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN') 
OPENAI_API_KEY = os.environ.get('OPENAI_API_TOKEN')
BOT_USERNAME = os.environ.get('BOT_USERNAME')
GITHUB_REPO = "github.com/valterm/dilly-dalle"
LOGLEVEL = getattr(logging, os.getenv('LOGGING_LEVEL', 'INFO'), logging.INFO)

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')