from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import stations, profiles, climatology

app = FastAPI(
    title="CMLRE Oceanographic Service",
    description="Handles CTD and oceanographic data processing",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(stations.router, prefix="/api/v1/oceanography", tags=["Stations"])
app.include_router(profiles.router, prefix="/api/v1/oceanography", tags=["Profiles"])
app.include_router(climatology.router, prefix="/api/v1/oceanography", tags=["Climatology"])

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "oceanographic"}
