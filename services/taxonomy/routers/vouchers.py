from fastapi import APIRouter

router = APIRouter()

@router.get("/vouchers")
async def get_vouchers():
    return {"message": "Vouchers placeholder"}
