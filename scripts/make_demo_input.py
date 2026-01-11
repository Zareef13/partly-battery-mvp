#!/usr/bin/env python3
"""Generate a demo input CSV file."""
import csv
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
OUTPUT_FILE = BASE_DIR / "data" / "demo_input.csv"

demo_data = [
    {"MPN": "CR2032", "Manufacturer": "Panasonic"},
    {"MPN": "18650", "Manufacturer": "Samsung"},
    {"MPN": "AA", "Manufacturer": "Duracell"},
    {"MPN": "UNKNOWN123", "Manufacturer": ""},
]

with open(OUTPUT_FILE, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["MPN", "Manufacturer"])
    writer.writeheader()
    writer.writerows(demo_data)

print(f"Created demo input file: {OUTPUT_FILE}")

