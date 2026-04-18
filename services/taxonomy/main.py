from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import species, otolith, vouchers

app = FastAPI(
    title="CMLRE Taxonomy Service",
    description="Handles species identification and taxonomy data",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(species.router, prefix="/api/v1/taxonomy", tags=["Species"])
app.include_router(otolith.router, prefix="/api/v1/taxonomy", tags=["Otolith"])
app.include_router(vouchers.router, prefix="/api/v1/taxonomy", tags=["Vouchers"])

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "taxonomy"}
