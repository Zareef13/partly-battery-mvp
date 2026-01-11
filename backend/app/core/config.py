import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv(Path(__file__).parent.parent.parent.parent / ".env")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
BASE_DIR = Path(__file__).parent.parent.parent.parent
CACHE_DIR = BASE_DIR / "data" / "cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)

