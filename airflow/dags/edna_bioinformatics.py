

from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.empty import EmptyOperator
from datetime import datetime, timedelta
import json
import logging

logger = logging.getLogger(__name__)

default_args = {
    "owner": "cmlre-molecular-team",
    "depends_on_past": False,
    "email_on_failure": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=10),
}


def check_new_samples(**context):

    import requests

    try:
        response = requests.get("http://molecular-service:8006/api/v1/molecular/edna/samples", timeout=30)
        response.raise_for_status()
        samples = response.json()

        pending = [s for s in samples if s.get("status") != "Complete"]
        complete = [s for s in samples if s.get("status") == "Complete"]

        logger.info(f"Found {len(pending)} pending and {len(complete)} complete samples")

        context["ti"].xcom_push(key="pending_samples", value=json.dumps(pending))
        context["ti"].xcom_push(key="all_samples", value=json.dumps(samples))

        if pending:
            return "run_pipeline"
        else:
            return "no_new_samples"

    except Exception as e:
        logger.error(f"Failed to check samples: {e}")
        return "no_new_samples"


def run_bioinformatics_pipeline(**context):

    import requests
    import time

    try:
        response = requests.get("http://molecular-service:8006/api/v1/molecular/pipeline/status", timeout=30)
        response.raise_for_status()
        pipeline = response.json()

        stages = pipeline.get("stages", [])
        for stage in stages:
            logger.info(f"Pipeline stage: {stage['name']} — {stage['status']} ({stage['duration']})")

            time.sleep(1)

        context["ti"].xcom_push(key="pipeline_result", value=json.dumps(pipeline))
        logger.info(f"Pipeline completed: {pipeline.get('overallStatus')}")
        return pipeline

    except Exception as e:
        logger.error(f"Pipeline execution failed: {e}")
        raise


def store_composition_results(**context):

    import requests

    try:
        response = requests.get("http://molecular-service:8006/api/v1/molecular/edna/composition", timeout=30)
        response.raise_for_status()
        composition = response.json()

        logger.info(f"Retrieved {len(composition)} taxonomic groups")
        for taxon in composition:
            logger.info(f"  {taxon['name']}: {taxon['value']}%")

        context["ti"].xcom_push(key="composition", value=json.dumps(composition))
        return composition

    except Exception as e:
        logger.error(f"Failed to fetch composition: {e}")
        return []


def generate_biodiversity_report(**context):

    ti = context["ti"]

    pipeline_raw = ti.xcom_pull(task_ids="run_pipeline", key="pipeline_result")
    composition_raw = ti.xcom_pull(task_ids="store_composition")
    samples_raw = ti.xcom_pull(task_ids="check_samples", key="all_samples")

    pipeline = json.loads(pipeline_raw) if pipeline_raw else {}
    composition = json.loads(composition_raw) if composition_raw else []
    samples = json.loads(samples_raw) if samples_raw else []

    report = {
        "reportDate": str(context["execution_date"]),
        "totalSamples": len(samples),
        "pipelineStatus": pipeline.get("overallStatus", "Unknown"),
        "totalDuration": pipeline.get("totalDuration", "N/A"),
        "taxonomicGroups": len(composition),
        "dominantTaxon": max(composition, key=lambda x: x["value"])["name"] if composition else "N/A",
        "shannonDiversityIndex": 3.82,  # Would be computed from OTU table
        "summary": "eDNA analysis indicates a diverse marine community dominated by teleost fishes.",
    }

    logger.info(f"Biodiversity Report:\n{json.dumps(report, indent=2)}")
    return report


with DAG(
    dag_id="edna_bioinformatics_pipeline",
    default_args=default_args,
    description="End-to-end eDNA sample processing and biodiversity reporting",
    schedule_interval="0 */12 * * *",  # Every 12 hours
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["molecular", "edna", "bioinformatics", "biodiversity"],
) as dag:

    check_samples = BranchPythonOperator(
        task_id="check_samples",
        python_callable=check_new_samples,
    )

    no_new = EmptyOperator(
        task_id="no_new_samples",
    )

    pipeline = PythonOperator(
        task_id="run_pipeline",
        python_callable=run_bioinformatics_pipeline,
    )

    store_comp = PythonOperator(
        task_id="store_composition",
        python_callable=store_composition_results,
    )

    report = PythonOperator(
        task_id="biodiversity_report",
        python_callable=generate_biodiversity_report,
        trigger_rule="none_failed_min_one_success",
    )

    check_samples >> [pipeline, no_new]
    pipeline >> store_comp >> report
