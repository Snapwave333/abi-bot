import os
import hashlib
import logging
from rich.logging import RichHandler
from dotenv import load_dotenv

# Load env immediately
load_dotenv()

def setup_logging():
    """Configures logging to file and console."""
    logging.basicConfig(
        level="INFO",
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("bot.log"),
            RichHandler(rich_tracebacks=True, markup=True)
        ]
    )
    return logging.getLogger("ABI_Bot")

def generate_event_id(summary, start_dt, end_dt):
    """Generates a deterministic unique ID for deduplication."""
    base_str = f"{summary}{start_dt.isoformat()}{end_dt.isoformat()}"
    return hashlib.md5(base_str.encode('utf-8')).hexdigest()

def get_env(key, default=None, required=False):
    val = os.getenv(key, default)
    if required and not val:
        raise ValueError(f"Missing required environment variable: {key}")
    return val
