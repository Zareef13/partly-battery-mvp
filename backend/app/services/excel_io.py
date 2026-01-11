import io
import pandas as pd
from typing import List, Dict
from app.core.logging import logger


def read_input(file_bytes: bytes, filename: str) -> List[Dict[str, str]]:
    """Read Excel or CSV file and return list of items with mpn/manufacturer."""
    try:
        if filename.endswith(".xlsx") or filename.endswith(".xls"):
            df = pd.read_excel(io.BytesIO(file_bytes))
        elif filename.endswith(".csv"):
            df = pd.read_csv(io.BytesIO(file_bytes))
        else:
            raise ValueError(f"Unsupported file format: {filename}")

        items = []
        # Normalize column names (case-insensitive, strip whitespace)
        df.columns = df.columns.str.strip().str.lower()
        
        # Look for MPN column (mpn, part number, part_number, etc.)
        mpn_col = None
        for col in df.columns:
            if col in ["mpn", "part number", "part_number", "partnumber", "model", "model number"]:
                mpn_col = col
                break
        
        if mpn_col is None:
            raise ValueError("Could not find MPN column in file")
        
        # Look for manufacturer column
        mfr_col = None
        for col in df.columns:
            if col in ["manufacturer", "mfr", "brand", "maker", "vendor"]:
                mfr_col = col
                break
        
        for _, row in df.iterrows():
            mpn = str(row[mpn_col]).strip() if pd.notna(row[mpn_col]) else ""
            manufacturer = str(row[mfr_col]).strip() if mfr_col and pd.notna(row.get(mfr_col, "")) else ""
            if mpn:
                items.append({"mpn": mpn, "manufacturer": manufacturer})
        
        logger.info(f"Read {len(items)} items from {filename}")
        return items
    except Exception as e:
        logger.error(f"Error reading file {filename}: {e}")
        raise

