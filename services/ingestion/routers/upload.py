from fastapi import APIRouter, UploadFile, File, HTTPException
from datetime import datetime
import uuid
import os

router = APIRouter()

# Persists in-memory only — production should use a database
UPLOAD_REGISTRY: list[dict] = []
FORMAT_MAP = {
    ".csv": {"format": "CSV", "pipeline": "tabular_ingest", "description": "Comma-separated values — routed to tabular ingestion pipeline"},
    ".tsv": {"format": "TSV", "pipeline": "tabular_ingest", "description": "Tab-separated values — routed to tabular ingestion pipeline"},
    ".nc": {"format": "NetCDF", "pipeline": "oceanographic_ingest", "description": "Network Common Data Form — routed to oceanographic CTD pipeline"},
    ".nc4": {"format": "NetCDF4", "pipeline": "oceanographic_ingest", "description": "NetCDF4 format — routed to oceanographic CTD pipeline"},
    ".fasta": {"format": "FASTA", "pipeline": "molecular_ingest", "description": "FASTA nucleotide sequence — routed to eDNA bioinformatics pipeline"},
    ".fa": {"format": "FASTA", "pipeline": "molecular_ingest", "description": "FASTA nucleotide sequence — routed to eDNA bioinformatics pipeline"},
    ".fastq": {"format": "FASTQ", "pipeline": "molecular_ingest", "description": "FASTQ with quality scores — routed to eDNA bioinformatics pipeline"},
    ".json": {"format": "JSON", "pipeline": "generic_ingest", "description": "JSON document — routed to MongoDB document store"},
    ".xlsx": {"format": "Excel", "pipeline": "tabular_ingest", "description": "Microsoft Excel — routed to tabular ingestion pipeline"},
    ".geojson": {"format": "GeoJSON", "pipeline": "spatial_ingest", "description": "GeoJSON spatial data — routed to PostGIS spatial pipeline"},
}


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):

    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename provided")


    ext = os.path.splitext(file.filename)[1].lower()
    format_info = FORMAT_MAP.get(ext)

    if format_info is None:
        format_info = {
            "format": "Unknown",
            "pipeline": "manual_review",
            "description": f"Unrecognized extension '{ext}' — queued for manual review",
        }


    content = await file.read()
    size_bytes = len(content)


    upload_id = str(uuid.uuid4())[:8].upper()
    record = {
        "uploadId": f"UPL-{upload_id}",
        "filename": file.filename,
        "sizeBytes": size_bytes,
        "sizeHuman": _human_size(size_bytes),
        "detectedFormat": format_info["format"],
        "targetPipeline": format_info["pipeline"],
        "description": format_info["description"],
        "status": "Queued",
        "uploadedAt": datetime.utcnow().isoformat() + "Z",
        "contentType": file.content_type,
    }

    UPLOAD_REGISTRY.append(record)

    return {
        "message": "File accepted and queued for processing.",
        **record,
    }


@router.get("/uploads")
async def list_uploads():

    return UPLOAD_REGISTRY


@router.get("/formats")
async def list_supported_formats():

    return [
        {"extension": ext, **info}
        for ext, info in FORMAT_MAP.items()
    ]


def _human_size(size_bytes: int) -> str:

    for unit in ["B", "KB", "MB", "GB"]:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"
