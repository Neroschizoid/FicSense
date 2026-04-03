import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Telegram
    BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    
    # Paths
    CHROME_BINARY = os.getenv("CHROME_BINARY_PATH", "/usr/bin/google-chrome")
    CHROME_DRIVER = os.getenv("CHROME_DRIVER_PATH", "/usr/local/bin/chromedriver")
    RAW_DATA_DIR = "data/raw"
    PROCESSED_DATA_DIR = "data/processed"
    
    # Models
    EMBED_MODEL = os.getenv("EMBED_MODEL_NAME", "nomic-embed-text")
    OLLAMA_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

    # Scraper Settings
    DEFAULT_SCROLLS = 4

# Ensure directories exist on startup
os.makedirs(Config.RAW_DATA_DIR, exist_ok=True)
os.makedirs(Config.PROCESSED_DATA_DIR, exist_ok=True)
