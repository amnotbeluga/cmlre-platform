from fastapi import APIRouter

router = APIRouter()


CTD_PROFILES = {
    "AS-01": {
        "stationId": "AS-01",
        "stationName": "Arabian Sea Deep Buoy",
        "castDate": "2024-11-10T06:30:00Z",
        "maxDepth": 2000,
        "layers": [
            {"depth": 0, "temperature": 29.1, "salinity": 35.0, "dissolvedOxygen": 4.8, "chlorophyll": 0.3},
            {"depth": 10, "temperature": 28.5, "salinity": 35.1, "dissolvedOxygen": 4.7, "chlorophyll": 0.5},
            {"depth": 25, "temperature": 27.8, "salinity": 35.1, "dissolvedOxygen": 4.5, "chlorophyll": 0.8},
            {"depth": 50, "temperature": 26.2, "salinity": 35.3, "dissolvedOxygen": 4.2, "chlorophyll": 1.2},
            {"depth": 75, "temperature": 24.1, "salinity": 35.4, "dissolvedOxygen": 3.8, "chlorophyll": 0.9},
            {"depth": 100, "temperature": 22.1, "salinity": 35.5, "dissolvedOxygen": 3.4, "chlorophyll": 0.4},
            {"depth": 150, "temperature": 19.2, "salinity": 35.4, "dissolvedOxygen": 2.8, "chlorophyll": 0.2},
            {"depth": 200, "temperature": 16.8, "salinity": 35.2, "dissolvedOxygen": 2.1, "chlorophyll": 0.1},
            {"depth": 300, "temperature": 12.4, "salinity": 35.0, "dissolvedOxygen": 1.5, "chlorophyll": 0.05},
            {"depth": 500, "temperature": 8.9, "salinity": 34.9, "dissolvedOxygen": 1.2, "chlorophyll": 0.02},
            {"depth": 750, "temperature": 6.2, "salinity": 34.8, "dissolvedOxygen": 1.8, "chlorophyll": 0.01},
            {"depth": 1000, "temperature": 4.1, "salinity": 34.7, "dissolvedOxygen": 2.5, "chlorophyll": 0.01},
            {"depth": 1500, "temperature": 2.8, "salinity": 34.7, "dissolvedOxygen": 3.1, "chlorophyll": 0.0},
            {"depth": 2000, "temperature": 1.9, "salinity": 34.7, "dissolvedOxygen": 3.5, "chlorophyll": 0.0},
        ]
    },
    "BB-03": {
        "stationId": "BB-03",
        "stationName": "Bay of Bengal Mooring",
        "castDate": "2024-11-12T08:15:00Z",
        "maxDepth": 1000,
        "layers": [
            {"depth": 0, "temperature": 28.8, "salinity": 33.2, "dissolvedOxygen": 4.6, "chlorophyll": 0.4},
            {"depth": 10, "temperature": 28.5, "salinity": 33.3, "dissolvedOxygen": 4.5, "chlorophyll": 0.6},
            {"depth": 25, "temperature": 28.0, "salinity": 33.5, "dissolvedOxygen": 4.3, "chlorophyll": 1.0},
            {"depth": 50, "temperature": 26.8, "salinity": 34.0, "dissolvedOxygen": 3.9, "chlorophyll": 1.5},
            {"depth": 100, "temperature": 21.5, "salinity": 34.8, "dissolvedOxygen": 2.8, "chlorophyll": 0.6},
            {"depth": 200, "temperature": 15.2, "salinity": 35.0, "dissolvedOxygen": 1.4, "chlorophyll": 0.1},
            {"depth": 500, "temperature": 9.1, "salinity": 34.9, "dissolvedOxygen": 0.8, "chlorophyll": 0.02},
            {"depth": 1000, "temperature": 4.5, "salinity": 34.8, "dissolvedOxygen": 2.2, "chlorophyll": 0.01},
        ]
    },
    "LK-07": {
        "stationId": "LK-07",
        "stationName": "Lakshadweep Reef Monitor",
        "castDate": "2024-11-08T10:00:00Z",
        "maxDepth": 200,
        "layers": [
            {"depth": 0, "temperature": 29.5, "salinity": 35.2, "dissolvedOxygen": 5.0, "chlorophyll": 0.2},
            {"depth": 10, "temperature": 29.2, "salinity": 35.2, "dissolvedOxygen": 4.9, "chlorophyll": 0.4},
            {"depth": 25, "temperature": 28.8, "salinity": 35.3, "dissolvedOxygen": 4.7, "chlorophyll": 0.6},
            {"depth": 50, "temperature": 27.5, "salinity": 35.3, "dissolvedOxygen": 4.4, "chlorophyll": 0.9},
            {"depth": 100, "temperature": 24.2, "salinity": 35.5, "dissolvedOxygen": 3.8, "chlorophyll": 0.3},
            {"depth": 200, "temperature": 18.0, "salinity": 35.4, "dissolvedOxygen": 2.5, "chlorophyll": 0.1},
        ]
    },
    "AN-12": {
        "stationId": "AN-12",
        "stationName": "Andaman Deep Current Profiler",
        "castDate": "2024-11-14T07:45:00Z",
        "maxDepth": 1500,
        "layers": [
            {"depth": 0, "temperature": 29.0, "salinity": 33.8, "dissolvedOxygen": 4.7, "chlorophyll": 0.3},
            {"depth": 10, "temperature": 28.6, "salinity": 33.9, "dissolvedOxygen": 4.6, "chlorophyll": 0.5},
            {"depth": 50, "temperature": 27.0, "salinity": 34.2, "dissolvedOxygen": 4.1, "chlorophyll": 1.1},
            {"depth": 100, "temperature": 22.8, "salinity": 34.6, "dissolvedOxygen": 3.2, "chlorophyll": 0.5},
            {"depth": 200, "temperature": 16.5, "salinity": 34.9, "dissolvedOxygen": 1.8, "chlorophyll": 0.1},
            {"depth": 500, "temperature": 8.5, "salinity": 34.8, "dissolvedOxygen": 1.0, "chlorophyll": 0.02},
            {"depth": 1000, "temperature": 4.0, "salinity": 34.7, "dissolvedOxygen": 2.3, "chlorophyll": 0.01},
            {"depth": 1500, "temperature": 2.5, "salinity": 34.7, "dissolvedOxygen": 3.0, "chlorophyll": 0.0},
        ]
    },
}


@router.get("/profiles/{station_id}")
async def get_profile(station_id: str):

    profile = CTD_PROFILES.get(station_id)
    if profile is None:
        return {
            "error": f"No CTD profile found for station '{station_id}'",
            "availableStations": list(CTD_PROFILES.keys()),
        }
    return profile


@router.get("/profiles")
async def list_profiles():

    return [
        {
            "stationId": p["stationId"],
            "stationName": p["stationName"],
            "castDate": p["castDate"],
            "maxDepth": p["maxDepth"],
            "layerCount": len(p["layers"]),
        }
        for p in CTD_PROFILES.values()
    ]
