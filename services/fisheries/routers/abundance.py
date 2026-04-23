from fastapi import APIRouter

router = APIRouter()

ABUNDANCE_DATA = [
    {
        "surveyId": "SRV-2024-001",
        "date": "2024-10-15",
        "zone": "Zone A — Kerala Coast",
        "gearType": "Trawl Net",
        "speciesCount": 24,
        "totalBiomassKg": 845.2,
        "dominantSpecies": "Sardinella longiceps",
        "shannonDiversity": 2.89,
    },
    {
        "surveyId": "SRV-2024-002",
        "date": "2024-10-22",
        "zone": "Zone B — Karnataka Coast",
        "gearType": "Purse Seine",
        "speciesCount": 18,
        "totalBiomassKg": 1230.5,
        "dominantSpecies": "Rastrelliger kanagurta",
        "shannonDiversity": 2.45,
    },
    {
        "surveyId": "SRV-2024-003",
        "date": "2024-11-05",
        "zone": "Zone C — Tamil Nadu Coast",
        "gearType": "Gill Net",
        "speciesCount": 31,
        "totalBiomassKg": 562.8,
        "dominantSpecies": "Thunnus albacares",
        "shannonDiversity": 3.12,
    },
    {
        "surveyId": "SRV-2024-004",
        "date": "2024-11-18",
        "zone": "Zone D — Andhra Pradesh Coast",
        "gearType": "Trawl Net",
        "speciesCount": 22,
        "totalBiomassKg": 978.1,
        "dominantSpecies": "Sardinella longiceps",
        "shannonDiversity": 2.67,
    },
]


@router.get("/abundance")
async def get_abundance():

    return ABUNDANCE_DATA


@router.get("/abundance/summary")
async def get_abundance_summary():

    total_biomass = sum(s["totalBiomassKg"] for s in ABUNDANCE_DATA)
    avg_species = sum(s["speciesCount"] for s in ABUNDANCE_DATA) / len(ABUNDANCE_DATA)
    return {
        "totalSurveys": len(ABUNDANCE_DATA),
        "totalBiomassKg": round(total_biomass, 1),
        "avgSpeciesPerSurvey": round(avg_species, 1),
        "surveyCoverage": "4 coastal zones",
    }
