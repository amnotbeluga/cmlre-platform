from fastapi import APIRouter

router = APIRouter()

VOUCHER_SPECIMENS = [
    {
        "voucherId": "CMLRE-VS-001",
        "scientificName": "Sardinella longiceps",
        "commonName": "Indian Oil Sardine",
        "collectionDate": "2024-08-12",
        "collectionSite": "Kochi, Kerala — 9.97°N, 76.27°E",
        "collector": "Dr. Priya Nair",
        "preservationType": "10% Formalin → 70% Ethanol",
        "repositoryId": "CMLRE-NIO-MAR-2024-001",
        "tissueAvailable": True,
        "dnaExtracted": True,
        "genBankAccession": "ON456789",
        "standardLength_mm": 142,
        "totalLength_mm": 168,
        "weight_g": 28.5,
        "sex": "Female",
        "maturityStage": "IV (Mature)",
        "status": "Catalogued",
    },
    {
        "voucherId": "CMLRE-VS-002",
        "scientificName": "Rastrelliger kanagurta",
        "commonName": "Indian Mackerel",
        "collectionDate": "2024-08-15",
        "collectionSite": "Mangalore, Karnataka — 12.87°N, 74.88°E",
        "collector": "Dr. Arun Kumar",
        "preservationType": "95% Ethanol (direct)",
        "repositoryId": "CMLRE-NIO-MAR-2024-002",
        "tissueAvailable": True,
        "dnaExtracted": True,
        "genBankAccession": "ON456790",
        "standardLength_mm": 205,
        "totalLength_mm": 248,
        "weight_g": 156.2,
        "sex": "Male",
        "maturityStage": "III (Developing)",
        "status": "Catalogued",
    },
    {
        "voucherId": "CMLRE-VS-003",
        "scientificName": "Thunnus albacares",
        "commonName": "Yellowfin Tuna",
        "collectionDate": "2024-09-22",
        "collectionSite": "Thoothukudi, Tamil Nadu — 8.76°N, 78.13°E",
        "collector": "Dr. Meena Raj",
        "preservationType": "Frozen (-20°C)",
        "repositoryId": "CMLRE-NIO-MAR-2024-003",
        "tissueAvailable": True,
        "dnaExtracted": False,
        "genBankAccession": None,
        "standardLength_mm": 890,
        "totalLength_mm": 1050,
        "weight_g": 18500,
        "sex": "Male",
        "maturityStage": "V (Spawning)",
        "status": "Pending DNA extraction",
    },
    {
        "voucherId": "CMLRE-VS-004",
        "scientificName": "Acropora cervicornis",
        "commonName": "Staghorn Coral",
        "collectionDate": "2024-10-05",
        "collectionSite": "Lakshadweep — 10.57°N, 72.64°E",
        "collector": "Dr. Reshma Das",
        "preservationType": "Dried skeletal fragment + 95% Ethanol tissue",
        "repositoryId": "CMLRE-NIO-MAR-2024-004",
        "tissueAvailable": True,
        "dnaExtracted": True,
        "genBankAccession": "ON456791",
        "standardLength_mm": None,
        "totalLength_mm": None,
        "weight_g": 45.0,
        "sex": "N/A",
        "maturityStage": "N/A",
        "status": "Catalogued",
    },
]


@router.get("/vouchers")
async def get_vouchers():

    return VOUCHER_SPECIMENS


@router.get("/vouchers/{voucher_id}")
async def get_voucher_detail(voucher_id: str):

    for v in VOUCHER_SPECIMENS:
        if v["voucherId"] == voucher_id:
            return v
    return {"error": f"Voucher '{voucher_id}' not found"}


@router.get("/vouchers/stats")
async def get_voucher_stats():

    total = len(VOUCHER_SPECIMENS)
    dna_extracted = sum(1 for v in VOUCHER_SPECIMENS if v["dnaExtracted"])
    with_genbank = sum(1 for v in VOUCHER_SPECIMENS if v["genBankAccession"])
    return {
        "totalSpecimens": total,
        "dnaExtracted": dna_extracted,
        "genBankLinked": with_genbank,
        "pendingDNA": total - dna_extracted,
        "uniqueSpecies": len(set(v["scientificName"] for v in VOUCHER_SPECIMENS)),
    }
