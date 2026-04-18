from fastapi import APIRouter

router = APIRouter()

@router.get("/surveys")
async def get_surveys():
    return {"message": "Surveys placeholder"}
