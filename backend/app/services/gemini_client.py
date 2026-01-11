from typing import Optional
from app.core.config import GEMINI_API_KEY
from app.models.battery import BatteryRecord
from app.core.logging import logger


def generate_overview(record: BatteryRecord) -> str:
    """Generate overview using Gemini API, or return template if API key not available."""
    if not GEMINI_API_KEY:
        return _generate_template_overview(record)
    
    try:
        import google.generativeai as genai
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel("gemini-pro")
        
        # Build prompt from record fields
        fields = []
        if record.chemistry:
            fields.append(f"Chemistry: {record.chemistry}")
        if record.voltage_v:
            fields.append(f"Voltage: {record.voltage_v}V")
        if record.capacity:
            fields.append(f"Capacity: {record.capacity}")
        if record.form_factor:
            fields.append(f"Form Factor: {record.form_factor}")
        if record.dimensions:
            fields.append(f"Dimensions: {record.dimensions}")
        if record.rechargeable is not None:
            fields.append(f"Rechargeable: {record.rechargeable}")
        
        prompt = f"""Generate a brief 2-3 sentence overview for this battery:
MPN: {record.mpn}
Manufacturer: {record.manufacturer or 'N/A'}
{' | '.join(fields)}

Overview:"""
        
        response = model.generate_content(prompt)
        overview = response.text.strip()
        logger.info(f"Generated Gemini overview for {record.mpn}")
        return overview
    except Exception as e:
        logger.warning(f"Gemini API error for {record.mpn}: {e}, using template")
        return _generate_template_overview(record)


def _generate_template_overview(record: BatteryRecord) -> str:
    """Generate a simple template overview from record fields."""
    parts = []
    if record.chemistry:
        parts.append(record.chemistry)
    if record.voltage_v:
        parts.append(f"{record.voltage_v}V")
    if record.capacity:
        parts.append(f"{record.capacity} capacity")
    if record.form_factor:
        parts.append(record.form_factor)
    if record.rechargeable is not None:
        rechargeable_str = "rechargeable" if record.rechargeable else "non-rechargeable"
        parts.append(rechargeable_str)
    
    if parts:
        return f"{record.mpn} is a {' '.join(parts)} battery."
    return f"{record.mpn} battery specification."

