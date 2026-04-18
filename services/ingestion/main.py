from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import upload

app = FastAPI(
    title="CMLRE Ingestion Service",
    description="Handles file upload, format detection, and ETL routing",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(upload.router, prefix="/api/v1/ingest", tags=["Ingestion"])

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "ingestion"}
