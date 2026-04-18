from fastapi import APIRouter

router = APIRouter()

@router.post("/otolith/analyze")
async def analyze_otolith():
    return {"message": "Otolith analysis placeholder"}
