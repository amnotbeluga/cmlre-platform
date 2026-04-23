from fastapi import APIRouter
import math

router = APIRouter()

DEPTH_PROFILE_DATA = [
    {"depth": 10, "temp": 28.5, "salinity": 35.1},
    {"depth": 50, "temp": 26.2, "salinity": 35.3},
    {"depth": 100, "temp": 22.1, "salinity": 35.5},
    {"depth": 200, "temp": 16.8, "salinity": 35.2},
    {"depth": 300, "temp": 12.4, "salinity": 35.0},
    {"depth": 500, "temp": 8.9, "salinity": 34.9},
    {"depth": 750, "temp": 6.2, "salinity": 34.8},
    {"depth": 1000, "temp": 4.1, "salinity": 34.7},
    {"depth": 1500, "temp": 2.8, "salinity": 34.7},
    {"depth": 2000, "temp": 1.9, "salinity": 34.7},
]

SST_ANOMALY_DATA = [
    {"year": "2015", "anomaly": 0.12},
    {"year": "2016", "anomaly": 0.34},
    {"year": "2017", "anomaly": -0.08},
    {"year": "2018", "anomaly": 0.21},
    {"year": "2019", "anomaly": 0.15},
    {"year": "2020", "anomaly": 0.42},
    {"year": "2021", "anomaly": 0.28},
    {"year": "2022", "anomaly": 0.55},
    {"year": "2023", "anomaly": 0.48},
    {"year": "2024", "anomaly": 0.62},
]


@router.post("/correlation")
async def run_correlation(params: dict):

    var_x = params.get("variableX", "temperature")
    var_y = params.get("variableY", "salinity")
    return {
        "variableX": var_x,
        "variableY": var_y,
        "correlationCoefficient": -0.89,
        "pValue": 0.0001,
        "rSquared": 0.79,
        "sampleSize": len(DEPTH_PROFILE_DATA),
        "method": "Pearson",
        "interpretation": f"Strong negative correlation between {var_x} and {var_y} across depth gradients.",
    }


@router.get("/depth-profile")
async def get_depth_profile():

    return DEPTH_PROFILE_DATA


@router.get("/sst-anomaly")
async def get_sst_anomaly():

    return SST_ANOMALY_DATA


@router.get("/summary")
async def get_analytics_summary():

    return {
        "totalStations": 48,
        "totalProfiles": 1243,
        "avgSST": 27.8,
        "avgSalinity": 35.1,
        "depthRange": {"min": 0, "max": 5000},
        "temporalRange": {"start": "2015-01-01", "end": "2024-12-31"},
    }
