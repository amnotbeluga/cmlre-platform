from fastapi import APIRouter

router = APIRouter()

@router.get("/profiles/{station_id}")
async def get_profile(station_id: str):
    return {"message": f"Profile placeholder for {station_id}"}
