from fastapi import APIRouter

router = APIRouter()

@router.get("/stations")
async def get_stations():
    return [
        { "id": "AS-01", "name": "Arabian Sea Deep Buoy", "lat": 15.0, "lng": 69.0, "temp": 28.5, "salinity": 35.8, "status": "Active" },
        { "id": "AS-02", "name": "Coastal Monitor", "lat": 11.2, "lng": 74.5, "temp": 29.1, "salinity": 34.2, "status": "Warning" },
        { "id": "BB-01", "name": "Bay of Bengal Deep", "lat": 14.5, "lng": 88.0, "temp": 27.8, "salinity": 33.1, "status": "Active" },
        { "id": "BB-02", "name": "Andaman Monitor", "lat": 10.5, "lng": 92.5, "temp": 28.9, "salinity": 32.5, "status": "Offline" },
    ]
