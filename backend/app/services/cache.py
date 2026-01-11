import json
from pathlib import Path
from typing import Optional, Dict, Any
from app.core.config import CACHE_DIR
from app.core.logging import logger


def get_cached(mpn: str) -> Optional[Dict[str, Any]]:
    """Get cached battery record for MPN."""
    cache_file = CACHE_DIR / f"{mpn}.json"
    if cache_file.exists():
        try:
            with open(cache_file, "r") as f:
                data = json.load(f)
                logger.info(f"Cache hit for {mpn}")
                return data
        except Exception as e:
            logger.warning(f"Error reading cache for {mpn}: {e}")
    return None


def save_cached(mpn: str, record_dict: Dict[str, Any]) -> None:
    """Save battery record to cache."""
    cache_file = CACHE_DIR / f"{mpn}.json"
    try:
        with open(cache_file, "w") as f:
            json.dump(record_dict, f, indent=2)
        logger.info(f"Cached {mpn}")
    except Exception as e:
        logger.warning(f"Error saving cache for {mpn}: {e}")

