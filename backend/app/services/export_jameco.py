import io
import pandas as pd
from typing import List, Tuple
from app.models.battery import BatteryRecord
from app.core.logging import logger


# Export column order as specified
EXPORT_COLUMNS = [
    "MPN",
    "Manufacturer",
    "Title",
    "Overview",
    "Chemistry",
    "Voltage (V)",
    "Capacity",
    "Wh",
    "Form Factor",
    "Dimensions",
    "Termination",
    "Rechargeable",
    "Operating Temp",
    "Weight",
    "Datasheet URL",
    "Source URLs",
]


def export_to_jameco(records: List[BatteryRecord], format: str) -> Tuple[bytes, str]:
    """Export battery records to Jameco format (XLSX or CSV)."""
    # Convert records to DataFrame rows
    rows = []
    for record in records:
        row = {
            "MPN": record.mpn,
            "Manufacturer": record.manufacturer or "",
            "Title": record.title or "",
            "Overview": record.overview or "",
            "Chemistry": record.chemistry or "",
            "Voltage (V)": record.voltage_v if record.voltage_v is not None else "",
            "Capacity": record.capacity or "",
            "Wh": record.wh if record.wh is not None else "",
            "Form Factor": record.form_factor or "",
            "Dimensions": record.dimensions or "",
            "Termination": record.termination or "",
            "Rechargeable": "Yes" if record.rechargeable else ("No" if record.rechargeable is False else ""),
            "Operating Temp": record.operating_temp or "",
            "Weight": record.weight or "",
            "Datasheet URL": record.datasheet_url or "",
            "Source URLs": ", ".join(record.source_urls) if record.source_urls else "",
        }
        rows.append(row)
    
    df = pd.DataFrame(rows, columns=EXPORT_COLUMNS)
    
    # Export to requested format
    output = io.BytesIO()
    if format.lower() == "xlsx":
        df.to_excel(output, index=False, engine="openpyxl")
        content_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    elif format.lower() == "csv":
        df.to_csv(output, index=False)
        content_type = "text/csv"
    else:
        raise ValueError(f"Unsupported format: {format}")
    
    output.seek(0)
    logger.info(f"Exported {len(records)} records to {format.upper()}")
    return output.getvalue(), content_type

