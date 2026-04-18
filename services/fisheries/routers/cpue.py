from fastapi import APIRouter

router = APIRouter()

@router.get("/cpue")
async def get_cpue():
    return {"message": "CPUE placeholder"}
