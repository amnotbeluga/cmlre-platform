from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import edna, pipeline

app = FastAPI(
    title="CMLRE Molecular/eDNA Service",
    description="Handles eDNA sample submission and pipeline orchestration",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(edna.router, prefix="/api/v1/molecular", tags=["eDNA"])
app.include_router(pipeline.router, prefix="/api/v1/molecular", tags=["Pipeline"])

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "molecular"}
