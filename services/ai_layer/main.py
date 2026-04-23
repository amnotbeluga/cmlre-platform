from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import ai

app = FastAPI(
    title="CMLRE AI Layer Service",
    description="Handles AI functionalities like schema matching and NLP search",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ai.router, prefix="/api/v1/ai", tags=["AI"])

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "ai_layer"}
