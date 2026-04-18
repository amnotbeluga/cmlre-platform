from fastapi import APIRouter

router = APIRouter()

@router.get("/climatology")
async def get_climatology():
    return {"message": "Climatology placeholder"}
