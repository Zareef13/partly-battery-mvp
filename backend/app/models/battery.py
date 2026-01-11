from typing import List, Optional
from pydantic import BaseModel


class BatteryRecord(BaseModel):
    mpn: str
    manufacturer: Optional[str] = None
    title: Optional[str] = None
    overview: Optional[str] = None
    chemistry: Optional[str] = None
    voltage_v: Optional[float] = None
    capacity: Optional[str] = None
    wh: Optional[float] = None
    form_factor: Optional[str] = None
    dimensions: Optional[str] = None
    termination: Optional[str] = None
    rechargeable: Optional[bool] = None
    operating_temp: Optional[str] = None
    weight: Optional[str] = None
    datasheet_url: Optional[str] = None
    source_urls: List[str] = []
    warnings: List[str] = []


class EnrichItem(BaseModel):
    mpn: str
    manufacturer: str = ""


class EnrichRequest(BaseModel):
    items: List[EnrichItem]


class EnrichResult(BaseModel):
    record: BatteryRecord
    status: str  # "success" | "error"
    error: Optional[str] = None


class EnrichResponse(BaseModel):
    results: List[EnrichResult]


class ExportRequest(BaseModel):
    records: List[BatteryRecord]
    format: str  # "xlsx" | "csv"

