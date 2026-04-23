from fastapi import APIRouter

router = APIRouter()


MONTHLY_CLIMATOLOGY = [
    {"month": "Jan", "meanSST": 27.2, "meanSalinity": 35.1, "meanWindSpeed": 5.8, "mixedLayerDepth": 45},
    {"month": "Feb", "meanSST": 27.5, "meanSalinity": 35.0, "meanWindSpeed": 5.2, "mixedLayerDepth": 40},
    {"month": "Mar", "meanSST": 28.1, "meanSalinity": 35.0, "meanWindSpeed": 4.5, "mixedLayerDepth": 35},
    {"month": "Apr", "meanSST": 29.0, "meanSalinity": 34.9, "meanWindSpeed": 3.8, "mixedLayerDepth": 25},
    {"month": "May", "meanSST": 29.8, "meanSalinity": 34.8, "meanWindSpeed": 4.2, "mixedLayerDepth": 20},
    {"month": "Jun", "meanSST": 28.5, "meanSalinity": 34.5, "meanWindSpeed": 8.5, "mixedLayerDepth": 30},
    {"month": "Jul", "meanSST": 27.8, "meanSalinity": 34.2, "meanWindSpeed": 9.8, "mixedLayerDepth": 40},
    {"month": "Aug", "meanSST": 27.5, "meanSalinity": 34.0, "meanWindSpeed": 9.2, "mixedLayerDepth": 45},
    {"month": "Sep", "meanSST": 27.8, "meanSalinity": 34.3, "meanWindSpeed": 7.5, "mixedLayerDepth": 38},
    {"month": "Oct", "meanSST": 28.2, "meanSalinity": 34.6, "meanWindSpeed": 5.5, "mixedLayerDepth": 30},
    {"month": "Nov", "meanSST": 28.0, "meanSalinity": 34.8, "meanWindSpeed": 5.0, "mixedLayerDepth": 35},
    {"month": "Dec", "meanSST": 27.5, "meanSalinity": 35.0, "meanWindSpeed": 5.5, "mixedLayerDepth": 42},
]

REGIONS = {
    "arabian_sea": {"name": "Arabian Sea", "latRange": [8, 24], "lonRange": [55, 75], "avgSST": 28.1},
    "bay_of_bengal": {"name": "Bay of Bengal", "latRange": [5, 22], "lonRange": [78, 95], "avgSST": 28.4},
    "lakshadweep_sea": {"name": "Lakshadweep Sea", "latRange": [8, 14], "lonRange": [70, 77], "avgSST": 29.0},
    "andaman_sea": {"name": "Andaman Sea", "latRange": [6, 14], "lonRange": [92, 100], "avgSST": 28.8},
}


@router.get("/climatology")
async def get_climatology():

    return {
        "region": "Indian Ocean (composite)",
        "baselinePeriod": "1991-2020",
        "monthly": MONTHLY_CLIMATOLOGY,
    }


@router.get("/climatology/regions")
async def get_regions():

    return REGIONS


@router.get("/climatology/{region}")
async def get_regional_climatology(region: str):

    r = REGIONS.get(region)
    if r is None:
        return {"error": f"Unknown region '{region}'", "available": list(REGIONS.keys())}
    return {
        "region": r["name"],
        "baselinePeriod": "1991-2020",
        "averageSST": r["avgSST"],
        "latRange": r["latRange"],
        "lonRange": r["lonRange"],
        "monthly": MONTHLY_CLIMATOLOGY,
    }
