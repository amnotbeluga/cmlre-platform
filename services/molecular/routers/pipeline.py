from fastapi import APIRouter

router = APIRouter()

@router.get("/pipeline/status")
async def get_pipeline_status():
    return {"message": "Pipeline status placeholder"}
