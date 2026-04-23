from fastapi import APIRouter

router = APIRouter()

PIPELINE_STAGES = [
    {"name": "Quality Control (FastQC)", "status": "Complete", "duration": "2m 34s", "reads_in": 1_500_000, "reads_out": 1_245_832},
    {"name": "Adapter Trimming (Cutadapt)", "status": "Complete", "duration": "1m 12s", "reads_in": 1_245_832, "reads_out": 1_198_402},
    {"name": "Denoising (DADA2)", "status": "Complete", "duration": "8m 45s", "reads_in": 1_198_402, "reads_out": 347},
    {"name": "Taxonomic Assignment (BLAST)", "status": "Complete", "duration": "12m 03s", "reads_in": 347, "reads_out": 312},
    {"name": "Phylogenetic Tree (MAFFT)", "status": "Complete", "duration": "3m 22s", "reads_in": 312, "reads_out": 312},
]


@router.get("/pipeline/status")
async def get_pipeline_status():

    return {
        "pipelineId": "PIPE-2024-001",
        "sampleId": "EDNA-2024-001",
        "overallStatus": "Complete",
        "startedAt": "2024-11-16T08:30:00Z",
        "completedAt": "2024-11-16T09:02:00Z",
        "totalDuration": "32m 00s",
        "stages": PIPELINE_STAGES,
    }


@router.get("/pipeline/runs")
async def get_pipeline_runs():

    return [
        {"pipelineId": "PIPE-2024-001", "sampleId": "EDNA-2024-001", "status": "Complete", "date": "2024-11-16"},
        {"pipelineId": "PIPE-2024-002", "sampleId": "EDNA-2024-002", "status": "Complete", "date": "2024-12-03"},
        {"pipelineId": "PIPE-2025-001", "sampleId": "EDNA-2025-011", "status": "Running", "date": "2025-01-10"},
    ]
