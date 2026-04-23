from fastapi import APIRouter
import random
import uuid

router = APIRouter()


EDNA_COMPOSITION = [
    {"name": "Teleostei (Bony Fish)", "value": 45, "color": "#0ea5e9"},
    {"name": "Crustacea", "value": 20, "color": "#8b5cf6"},
    {"name": "Cnidaria (Jellyfish)", "value": 12, "color": "#06b6d4"},
    {"name": "Mollusca", "value": 10, "color": "#10b981"},
    {"name": "Echinodermata", "value": 8, "color": "#f59e0b"},
    {"name": "Unclassified", "value": 5, "color": "#64748b"},
]

SAMPLE_DB = {
    "EDNA-2024-001": {
        "sampleId": "EDNA-2024-001",
        "location": "Arabian Sea — Station AS-01",
        "collectionDate": "2024-11-15",
        "depth": "10m",
        "waterVolume": "2L",
        "filterType": "0.45μm Sterivex",
        "status": "Complete",
        "totalReads": 1_245_832,
        "uniqueOTUs": 347,
        "shannonIndex": 3.82,
    },
    "EDNA-2024-002": {
        "sampleId": "EDNA-2024-002",
        "location": "Bay of Bengal — Station BB-03",
        "collectionDate": "2024-12-02",
        "depth": "50m",
        "waterVolume": "2L",
        "filterType": "0.22μm Sterivex",
        "status": "Complete",
        "totalReads": 982_114,
        "uniqueOTUs": 289,
        "shannonIndex": 3.45,
    },
}

def _generate_sequence(length: int = 200) -> str:

    return "".join(random.choice("ATCG") for _ in range(length))


@router.get("/edna/composition")
async def get_edna_composition():

    return EDNA_COMPOSITION


@router.get("/edna/samples")
async def get_edna_samples():

    return list(SAMPLE_DB.values())


@router.post("/edna/submit")
async def submit_edna():

    new_id = f"EDNA-{random.randint(2025, 2030)}-{random.randint(1, 999):03d}"
    return {
        "sampleId": new_id,
        "status": "Queued",
        "message": "Sample accepted for bioinformatics pipeline processing.",
    }


@router.get("/edna/{sample_id}/results")
async def get_edna_results(sample_id: str):

    sample = SAMPLE_DB.get(sample_id)
    if sample is None:

        sample = {
            "sampleId": sample_id,
            "location": "Unknown",
            "status": "Processing",
            "totalReads": 0,
            "uniqueOTUs": 0,
            "shannonIndex": 0.0,
        }
    return {
        **sample,
        "composition": EDNA_COMPOSITION,
        "sequence": _generate_sequence(200),
    }


@router.get("/edna/sequence")
async def get_edna_sequence():

    seq = _generate_sequence(300)
    return {
        "sequence": seq,
        "length": len(seq),
        "gcContent": round((seq.count("G") + seq.count("C")) / len(seq) * 100, 1),
    }
