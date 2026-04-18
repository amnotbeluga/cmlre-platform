from fastapi import APIRouter

router = APIRouter()

@router.get("/abundance")
async def get_abundance():
    return {"message": "Abundance placeholder"}
