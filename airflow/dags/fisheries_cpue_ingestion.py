

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import json
import logging

logger = logging.getLogger(__name__)

default_args = {
    "owner": "cmlre-fisheries-team",
    "depends_on_past": False,
    "email_on_failure": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}


def fetch_cpue_data(**context):

    import requests

    try:
        response = requests.get("http://fisheries-service:8004/api/v1/fisheries/cpue", timeout=30)
        response.raise_for_status()
        data = response.json()
        logger.info(f"Fetched {len(data)} CPUE records")
        return json.dumps(data)
    except Exception as e:
        logger.error(f"Failed to fetch CPUE data: {e}")
        return "[]"


def fetch_abundance_data(**context):

    import requests

    try:
        response = requests.get("http://fisheries-service:8004/api/v1/fisheries/abundance", timeout=30)
        response.raise_for_status()
        data = response.json()
        logger.info(f"Fetched {len(data)} abundance records")
        return json.dumps(data)
    except Exception as e:
        logger.error(f"Failed to fetch abundance data: {e}")
        return "[]"


def compute_aggregates(**context):

    ti = context["ti"]

    cpue_raw = ti.xcom_pull(task_ids="fetch_cpue")
    abundance_raw = ti.xcom_pull(task_ids="fetch_abundance")

    cpue_data = json.loads(cpue_raw) if cpue_raw else []
    abundance_data = json.loads(abundance_raw) if abundance_raw else []


    species_totals = {}
    for record in cpue_data:
        for species in ["Sardines", "Mackerel", "Tuna"]:
            if species in record:
                species_totals[species] = species_totals.get(species, 0) + record[species]


    total_biomass = sum(r.get("totalBiomassKg", 0) for r in abundance_data)
    total_surveys = len(abundance_data)

    aggregates = {
        "date": str(context["execution_date"].date()),
        "cpueBySpecies": species_totals,
        "totalZones": len(cpue_data),
        "totalBiomassKg": total_biomass,
        "totalSurveys": total_surveys,
    }

    logger.info(f"Aggregates computed: {json.dumps(aggregates, indent=2)}")
    ti.xcom_push(key="aggregates", value=json.dumps(aggregates))
    return aggregates


def store_aggregates(**context):

    ti = context["ti"]
    raw = ti.xcom_pull(task_ids="compute_aggregates", key="aggregates")
    aggregates = json.loads(raw) if raw else {}

    if not aggregates:
        logger.info("No aggregates to store")
        return

    import psycopg2

    conn = psycopg2.connect(
        host="timescaledb", port=5432,
        user="cmlre", password="cmlrepassword", dbname="cmlredb"
    )
    conn.autocommit = True
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS fisheries_daily_summary (
            date DATE PRIMARY KEY,
            sardine_total INTEGER DEFAULT 0,
            mackerel_total INTEGER DEFAULT 0,
            tuna_total INTEGER DEFAULT 0,
            total_zones INTEGER DEFAULT 0,
            total_biomass_kg DOUBLE PRECISION DEFAULT 0,
            total_surveys INTEGER DEFAULT 0,
            computed_at TIMESTAMPTZ DEFAULT NOW()
        );
    """)

    species = aggregates.get("cpueBySpecies", {})
    cursor.execute("""
        INSERT INTO fisheries_daily_summary (date, sardine_total, mackerel_total, tuna_total, total_zones, total_biomass_kg, total_surveys)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (date) DO UPDATE SET
            sardine_total = EXCLUDED.sardine_total,
            mackerel_total = EXCLUDED.mackerel_total,
            tuna_total = EXCLUDED.tuna_total,
            total_zones = EXCLUDED.total_zones,
            total_biomass_kg = EXCLUDED.total_biomass_kg,
            total_surveys = EXCLUDED.total_surveys,
            computed_at = NOW()
    """, (
        aggregates.get("date"),
        species.get("Sardines", 0),
        species.get("Mackerel", 0),
        species.get("Tuna", 0),
        aggregates.get("totalZones", 0),
        aggregates.get("totalBiomassKg", 0),
        aggregates.get("totalSurveys", 0),
    ))

    logger.info(f"Stored daily fisheries summary for {aggregates.get('date')}")
    conn.close()


with DAG(
    dag_id="fisheries_cpue_ingestion",
    default_args=default_args,
    description="Daily CPUE and abundance data aggregation pipeline",
    schedule_interval="0 2 * * *",  # Daily at 02:00 UTC
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["fisheries", "cpue", "abundance", "ingestion"],
) as dag:

    fetch_cpue = PythonOperator(
        task_id="fetch_cpue",
        python_callable=fetch_cpue_data,
    )

    fetch_abundance = PythonOperator(
        task_id="fetch_abundance",
        python_callable=fetch_abundance_data,
    )

    aggregate = PythonOperator(
        task_id="compute_aggregates",
        python_callable=compute_aggregates,
    )

    store = PythonOperator(
        task_id="store_aggregates",
        python_callable=store_aggregates,
    )

    [fetch_cpue, fetch_abundance] >> aggregate >> store
