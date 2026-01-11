from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import Response
from app.models.battery import EnrichRequest, EnrichResponse, EnrichResult, ExportRequest
from app.services.excel_io import read_input
from app.services.enrich import enrich_item
from app.services.export_jameco import export_to_jameco
from app.core.logging import logger

router = APIRouter()


@router.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "ok"}


@router.post("/upload")
async def upload(file: UploadFile = File(...)):
    """Upload Excel or CSV file and extract MPNs and manufacturers."""
    try:
        file_bytes = await file.read()
        items = read_input(file_bytes, file.filename)
        
        mpns = [item["mpn"] for item in items]
        manufacturers = [item["manufacturer"] for item in items if item.get("manufacturer")]
        
        return {
            "mpns": mpns,
            "manufacturers": list(set(manufacturers)) if manufacturers else []
        }
    except Exception as e:
        logger.error(f"Upload error: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/enrich", response_model=EnrichResponse)
async def enrich(request: EnrichRequest):
    """Enrich battery items and return enriched records."""
    results = []
    
    for item in request.items:
        try:
            record, warnings = enrich_item(item)
            results.append(EnrichResult(
                record=record,
                status="success",
                error=None
            ))
        except Exception as e:
            logger.error(f"Error enriching {item.mpn}: {e}")
            from app.models.battery import BatteryRecord
            error_record = BatteryRecord(mpn=item.mpn, manufacturer=item.manufacturer)
            results.append(EnrichResult(
                record=error_record,
                status="error",
                error=str(e)
            ))
    
    return EnrichResponse(results=results)


@router.post("/export")
async def export(request: ExportRequest):
    """Export battery records to Jameco format (XLSX or CSV)."""
    try:
        file_bytes, content_type = export_to_jameco(request.records, request.format)
        extension = request.format.lower()
        filename = f"battery_export.{extension}"
        
        return Response(
            content=file_bytes,
            media_type=content_type,
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    except Exception as e:
        logger.error(f"Export error: {e}")
        raise HTTPException(status_code=400, detail=str(e))

