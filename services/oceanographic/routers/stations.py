from fastapi import APIRouter

router = APIRouter()

@router.get("/stations")
async def get_stations():
    return {"message": "Stations placeholder"}
