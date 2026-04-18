from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import cpue, abundance, surveys

app = FastAPI(
    title="CMLRE Fisheries Service",
    description="Handles fisheries catch and abundance data",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(cpue.router, prefix="/api/v1/fisheries", tags=["CPUE"])
app.include_router(abundance.router, prefix="/api/v1/fisheries", tags=["Abundance"])
app.include_router(surveys.router, prefix="/api/v1/fisheries", tags=["Surveys"])

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "fisheries"}
