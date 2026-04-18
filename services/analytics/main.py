from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import correlation

app = FastAPI(
    title="CMLRE Analytics Service",
    description="Handles statistical correlations and GAM modeling",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(correlation.router, prefix="/api/v1/analytics", tags=["Correlation"])

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "analytics"}
