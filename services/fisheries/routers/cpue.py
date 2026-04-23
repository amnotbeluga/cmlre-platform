from fastapi import APIRouter

router = APIRouter()

@router.get("/cpue")
async def get_cpue():
    return [
        { "zone": "Zone A", "Sardines": 4000, "Mackerel": 2400, "Tuna": 2400 },
        { "zone": "Zone B", "Sardines": 3000, "Mackerel": 1398, "Tuna": 2210 },
        { "zone": "Zone C", "Sardines": 2000, "Mackerel": 9800, "Tuna": 2290 },
        { "zone": "Zone D", "Sardines": 2780, "Mackerel": 3908, "Tuna": 2000 },
        { "zone": "Zone E", "Sardines": 1890, "Mackerel": 4800, "Tuna": 2181 },
        { "zone": "Zone F", "Sardines": 2390, "Mackerel": 3800, "Tuna": 2500 },
    ]
