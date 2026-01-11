from typing import Dict, Any, Optional


# Common field mappings for normalization
FIELD_MAPPINGS = {
    "nominal voltage": "voltage_v",
    "voltage": "voltage_v",
    "voltage (v)": "voltage_v",
    "capacity": "capacity",
    "capacity (mah)": "capacity",
    "capacity (ah)": "capacity",
    "chemistry": "chemistry",
    "battery type": "chemistry",
    "type": "chemistry",
    "size": "form_factor",
    "form factor": "form_factor",
    "dimensions": "dimensions",
    "size dimensions": "dimensions",
    "termination": "termination",
    "rechargeable": "rechargeable",
    "temp range": "operating_temp",
    "operating temp": "operating_temp",
    "operating temperature": "operating_temp",
    "weight": "weight",
    "datasheet": "datasheet_url",
    "datasheet url": "datasheet_url",
}


def normalize_candidates(candidates: Dict[str, Any], mpn: str, manufacturer: str = "") -> Dict[str, Any]:
    """Normalize candidate fields into canonical battery schema."""
    record = {
        "mpn": mpn,
        "manufacturer": manufacturer or candidates.get("manufacturer", ""),
        "title": candidates.get("title", ""),
        "chemistry": candidates.get("chemistry", ""),
        "voltage_v": _parse_float(candidates.get("voltage_v") or candidates.get("voltage") or candidates.get("nominal_voltage")),
        "capacity": candidates.get("capacity", ""),
        "wh": _parse_float(candidates.get("wh") or candidates.get("watt_hours")),
        "form_factor": candidates.get("form_factor") or candidates.get("size", ""),
        "dimensions": candidates.get("dimensions", ""),
        "termination": candidates.get("termination", ""),
        "rechargeable": _parse_bool(candidates.get("rechargeable")),
        "operating_temp": candidates.get("operating_temp") or candidates.get("temp_range", ""),
        "weight": candidates.get("weight", ""),
        "datasheet_url": candidates.get("datasheet_url") or candidates.get("datasheet", ""),
        "source_urls": candidates.get("source_urls", []),
        "warnings": candidates.get("warnings", []),
    }
    
    # Apply field mappings if candidates use different keys
    for key, value in candidates.items():
        normalized_key = FIELD_MAPPINGS.get(key.lower())
        if normalized_key and not record.get(normalized_key):
            if normalized_key == "voltage_v":
                record["voltage_v"] = _parse_float(value)
            elif normalized_key == "rechargeable":
                record["rechargeable"] = _parse_bool(value)
            else:
                record[normalized_key] = value
    
    return record


def _parse_float(value: Any) -> Optional[float]:
    """Parse float value, handling strings."""
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        try:
            # Remove units and extract number
            cleaned = value.replace("V", "").replace("v", "").replace("Wh", "").replace("wh", "").strip()
            return float(cleaned)
        except:
            return None
    return None


def _parse_bool(value: Any) -> Optional[bool]:
    """Parse boolean value."""
    if value is None:
        return None
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.lower() in ("true", "yes", "1", "rechargeable", "y")
    return bool(value)

