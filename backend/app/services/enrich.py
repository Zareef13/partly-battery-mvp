from typing import Dict, Any, Tuple, List
from app.models.battery import BatteryRecord, EnrichItem
from app.services.cache import get_cached, save_cached
from app.services.normalize import normalize_candidates
from app.services.gemini_client import generate_overview
from app.core.logging import logger


def fetch_candidates(mpn: str, manufacturer: str = "") -> Dict[str, Any]:
    """
    Stub implementation that returns deterministic candidate fields for sample MPNs.
    This architecture allows easy swapping with real search/scraping later.
    """
    mpn_upper = mpn.upper()
    
    # Sample deterministic data for demo
    stub_data = {
        "CR2032": {
            "title": "CR2032 3V Lithium Coin Cell Battery",
            "chemistry": "Lithium",
            "voltage_v": 3.0,
            "capacity": "220mAh",
            "form_factor": "Coin Cell",
            "dimensions": "20mm x 3.2mm",
            "rechargeable": False,
            "operating_temp": "-30°C to +60°C",
            "weight": "3.1g",
            "source_urls": ["https://example.com/cr2032"],
        },
        "18650": {
            "title": "18650 Lithium Ion Battery",
            "chemistry": "Lithium-Ion",
            "voltage_v": 3.7,
            "capacity": "2600mAh",
            "wh": 9.62,
            "form_factor": "Cylindrical",
            "dimensions": "18mm x 65mm",
            "termination": "Button Top",
            "rechargeable": True,
            "operating_temp": "0°C to +45°C",
            "weight": "45g",
            "source_urls": ["https://example.com/18650"],
        },
        "AA": {
            "title": "AA Alkaline Battery",
            "chemistry": "Alkaline",
            "voltage_v": 1.5,
            "capacity": "2500mAh",
            "form_factor": "AA",
            "dimensions": "14.5mm x 50.5mm",
            "rechargeable": False,
            "operating_temp": "-18°C to +55°C",
            "weight": "23g",
            "source_urls": ["https://example.com/aa"],
        },
    }
    
    # Check if we have stub data for this MPN
    if mpn_upper in stub_data:
        data = stub_data[mpn_upper].copy()
        if manufacturer:
            data["manufacturer"] = manufacturer
        return data
    
    # Return empty fields for unknown MPNs
    result = {}
    if manufacturer:
        result["manufacturer"] = manufacturer
    return result


def enrich_item(item: EnrichItem) -> Tuple[BatteryRecord, List[str]]:
    """
    Enrich a single battery item.
    Returns (BatteryRecord, warnings_list)
    """
    warnings = []
    mpn = item.mpn.strip()
    manufacturer = item.manufacturer.strip() if item.manufacturer else ""
    
    # 1. Check cache
    cached = get_cached(mpn)
    if cached:
        record = BatteryRecord(**cached)
        return record, []
    
    try:
        # 2. Fetch candidates (stub)
        candidates = fetch_candidates(mpn, manufacturer)
        
        # 3. Normalize into canonical schema
        record_dict = normalize_candidates(candidates, mpn, manufacturer)
        
        # 4. Generate overview
        temp_record = BatteryRecord(**record_dict)
        overview = generate_overview(temp_record)
        record_dict["overview"] = overview
        
        # Create final record
        record = BatteryRecord(**record_dict)
        
        # 5. Save to cache
        save_cached(mpn, record.model_dump())
        
        return record, warnings
    except Exception as e:
        logger.error(f"Error enriching {mpn}: {e}")
        warnings.append(f"Enrichment error: {str(e)}")
        # Return minimal record on error
        record = BatteryRecord(mpn=mpn, manufacturer=manufacturer, warnings=warnings)
        return record, warnings

