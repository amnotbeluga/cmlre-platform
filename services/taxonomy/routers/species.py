from fastapi import APIRouter

router = APIRouter()

@router.get("/species")
async def get_species():
    return {"message": "Species placeholder"}
