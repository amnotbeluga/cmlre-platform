from fastapi import APIRouter
from typing import Optional

router = APIRouter()


KNOWLEDGE_BASE = [

    {"type": "station", "id": "AS-01", "title": "Arabian Sea Deep Buoy", "description": "Continuous monitoring station at 15°N 69°E. Measures SST, salinity, dissolved oxygen, and current velocity at 10m, 50m, and 200m depths.", "tags": ["arabian sea", "buoy", "sst", "salinity", "current", "deep water"]},
    {"type": "station", "id": "BB-03", "title": "Bay of Bengal Mooring", "description": "Fixed mooring station at 13°N 84°E. Tracks monsoon-driven upwelling events and thermocline depth variations.", "tags": ["bay of bengal", "mooring", "monsoon", "upwelling", "thermocline"]},
    {"type": "station", "id": "LK-07", "title": "Lakshadweep Reef Monitor", "description": "Coral reef monitoring station at 10.5°N 72.6°E. Tracks reef bleaching indicators and pH levels.", "tags": ["lakshadweep", "coral", "reef", "bleaching", "ph", "acidification"]},
    {"type": "station", "id": "AN-12", "title": "Andaman Deep Current Profiler", "description": "ADCP station monitoring deep ocean currents and internal wave activity in the Andaman Sea.", "tags": ["andaman", "current", "adcp", "deep ocean", "internal waves"]},


    {"type": "species", "id": "TAX-104", "title": "Aequorea victoria (Crystal Jellyfish)", "description": "Bioluminescent hydrozoan jellyfish found off the west coast of North America. Source of Green Fluorescent Protein (GFP).", "tags": ["jellyfish", "bioluminescent", "gfp", "cnidaria", "hydrozoan"]},
    {"type": "species", "id": "TAX-211", "title": "Acropora cervicornis (Staghorn Coral)", "description": "Branching stony coral. Critically endangered due to bleaching, disease, and ocean acidification.", "tags": ["coral", "endangered", "bleaching", "acropora", "scleractinia"]},
    {"type": "species", "id": "TAX-893", "title": "Chaetoceros sp. (Diatom)", "description": "Microscopic phytoplankton with silica frustules. Major primary producer and carbon sink in tropical oceans.", "tags": ["phytoplankton", "diatom", "plankton", "carbon", "primary producer", "silica"]},
    {"type": "species", "id": "TAX-501", "title": "Sardinella longiceps (Indian Oil Sardine)", "description": "Small pelagic fish, most commercially important species along the Indian southwest coast.", "tags": ["sardine", "pelagic", "fisheries", "commercial", "kerala", "india"]},
    {"type": "species", "id": "TAX-502", "title": "Rastrelliger kanagurta (Indian Mackerel)", "description": "Pelagic schooling fish found across the Indo-Pacific. Key species in Indian marine fisheries.", "tags": ["mackerel", "pelagic", "fisheries", "commercial", "indo-pacific"]},
    {"type": "species", "id": "TAX-503", "title": "Thunnus albacares (Yellowfin Tuna)", "description": "Large migratory tuna found in tropical and subtropical oceans. Important for both commercial and sport fisheries.", "tags": ["tuna", "yellowfin", "pelagic", "migratory", "commercial"]},


    {"type": "fisheries", "id": "ZONE-A", "title": "Zone A — Kerala Coast", "description": "Southwest coast fisheries zone. High sardine and mackerel yields during monsoon season. Primary landing centers: Kochi, Kozhikode.", "tags": ["kerala", "sardine", "mackerel", "monsoon", "trawl", "southwest"]},
    {"type": "fisheries", "id": "ZONE-B", "title": "Zone B — Karnataka Coast", "description": "Western coast zone known for purse seine operations targeting mackerel and sardine shoals.", "tags": ["karnataka", "purse seine", "mackerel", "sardine", "western coast"]},
    {"type": "fisheries", "id": "ZONE-C", "title": "Zone C — Tamil Nadu Coast", "description": "Southeast coast zone with diverse fisheries. Notable for tuna longlining and gill net operations.", "tags": ["tamil nadu", "tuna", "gill net", "longline", "southeast"]},


    {"type": "edna", "id": "EDNA-2024-001", "title": "eDNA Sample — Arabian Sea 10m", "description": "Environmental DNA water sample collected at 10m depth from Arabian Sea Station AS-01. 1,245,832 total reads, 347 unique OTUs identified.", "tags": ["edna", "arabian sea", "metabarcoding", "otu", "biodiversity"]},


    {"type": "concept", "id": "CONCEPT-SST", "title": "Sea Surface Temperature (SST) Anomaly", "description": "Deviation of SST from the long-term mean. Positive anomalies indicate warming trends linked to El Niño, climate change, and coral bleaching events.", "tags": ["sst", "temperature", "anomaly", "climate", "warming", "el nino", "bleaching"]},
    {"type": "concept", "id": "CONCEPT-CPUE", "title": "Catch Per Unit Effort (CPUE)", "description": "Standard fisheries metric measuring the quantity of fish caught per unit of fishing effort. Used as an index of fish stock abundance.", "tags": ["cpue", "fisheries", "catch", "effort", "abundance", "stock"]},
]


def _score_result(item: dict, query_terms: list[str]) -> float:

    score = 0.0
    text = f"{item['title']} {item['description']}".lower()
    tags = " ".join(item.get("tags", []))

    for term in query_terms:
        t = term.lower()
        if t in item["title"].lower():
            score += 10.0
        if t in tags:
            score += 5.0
        if t in text:
            score += 2.0
    return score


@router.get("/search")
async def semantic_search(query: str, limit: int = 10):

    terms = query.strip().split()
    if not terms:
        return {"query": query, "results": [], "totalResults": 0}

    scored = []
    for item in KNOWLEDGE_BASE:
        s = _score_result(item, terms)
        if s > 0:
            scored.append({**item, "_score": s})

    scored.sort(key=lambda x: x["_score"], reverse=True)
    results = scored[:limit]


    for r in results:
        r.pop("_score", None)
        r.pop("tags", None)

    return {
        "query": query,
        "results": results,
        "totalResults": len(results),
    }


@router.post("/schema-match")
async def schema_match(payload: dict):

    columns = payload.get("columns", [])

    KNOWN_MAPPINGS = {
        "lat": "latitude", "latitude": "latitude", "lon": "longitude", "lng": "longitude", "longitude": "longitude",
        "temp": "temperature_celsius", "temperature": "temperature_celsius", "sst": "sea_surface_temperature",
        "sal": "salinity_psu", "salinity": "salinity_psu",
        "depth": "depth_meters", "date": "datetime", "time": "datetime", "timestamp": "datetime",
        "species": "scientific_name", "weight": "weight_kg", "catch": "catch_weight_kg",
        "cpue": "catch_per_unit_effort", "station": "station_id", "gear": "gear_type",
    }

    matches = []
    for col in columns:
        col_lower = col.lower().strip()
        mapped = KNOWN_MAPPINGS.get(col_lower)
        matches.append({
            "original": col,
            "mappedField": mapped or "unknown",
            "confidence": 0.95 if mapped else 0.0,
        })

    return {"columns": matches}
