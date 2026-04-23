

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.http.operators.http import SimpleHttpOperator
from datetime import datetime, timedelta
import json
import logging

logger = logging.getLogger(__name__)

default_args = {
    "owner": "cmlre-data-team",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}


def validate_ctd_data(**context):

    ti = context["ti"]
    raw_data = ti.xcom_pull(task_ids="fetch_station_data")

    if not raw_data:
        logger.warning("No data received from stations API")
        return []

    data = json.loads(raw_data) if isinstance(raw_data, str) else raw_data

    validated = []
    rejected = 0

    for record in data:
        temp = record.get("temp")
        salinity = record.get("salinity")

        if temp is None or salinity is None:
            rejected += 1
            continue
        if not (-2.0 <= temp <= 35.0):
            logger.warning(f"Station {record.get('id')}: Temperature {temp}°C out of range")
            rejected += 1
            continue
        if not (0.0 <= salinity <= 42.0):
            logger.warning(f"Station {record.get('id')}: Salinity {salinity} PSU out of range")
            rejected += 1
            continue

        validated.append(record)

    logger.info(f"QC complete: {len(validated)} passed, {rejected} rejected")
    ti.xcom_push(key="validated_data", value=json.dumps(validated))
    ti.xcom_push(key="qc_stats", value={"passed": len(validated), "rejected": rejected})
    return validated


def load_to_timescaledb(**context):

    ti = context["ti"]
    raw = ti.xcom_pull(task_ids="validate_data", key="validated_data")
    data = json.loads(raw) if raw else []

    if not data:
        logger.info("No validated data to load")
        return

    import psycopg2

    conn = psycopg2.connect(
        host="timescaledb", port=5432,
        user="cmlre", password="cmlrepassword", dbname="cmlredb"
    )
    conn.autocommit = True
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ctd_observations (
            time TIMESTAMPTZ NOT NULL DEFAULT NOW(),
            station_id VARCHAR(20),
            station_name VARCHAR(200),
            latitude DOUBLE PRECISION,
            longitude DOUBLE PRECISION,
            temperature DOUBLE PRECISION,
            salinity DOUBLE PRECISION
        );
    """)

    for record in data:
        cursor.execute("""
            INSERT INTO ctd_observations (station_id, station_name, latitude, longitude, temperature, salinity)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            record.get("id"), record.get("name"),
            record.get("lat"), record.get("lng"),
            record.get("temp"), record.get("salinity"),
        ))

    logger.info(f"Loaded {len(data)} records into ctd_observations")
    conn.close()


def generate_summary_report(**context):

    ti = context["ti"]
    qc_stats = ti.xcom_pull(task_ids="validate_data", key="qc_stats")

    report = {
        "dagRun": context["run_id"],
        "executionDate": str(context["execution_date"]),
        "qcPassed": qc_stats.get("passed", 0) if qc_stats else 0,
        "qcRejected": qc_stats.get("rejected", 0) if qc_stats else 0,
        "status": "SUCCESS",
    }

    logger.info(f"Ingestion Report: {json.dumps(report, indent=2)}")
    return report


with DAG(
    dag_id="oceanographic_data_ingestion",
    default_args=default_args,
    description="Ingest CTD data from monitoring stations into TimescaleDB",
    schedule_interval="0 */6 * * *",  # Every 6 hours
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["oceanographic", "ctd", "ingestion"],
) as dag:

    fetch_data = SimpleHttpOperator(
        task_id="fetch_station_data",
        http_conn_id="oceanographic_service",
        endpoint="/api/v1/oceanography/stations",
        method="GET",
        response_check=lambda response: response.status_code == 200,
        log_response=True,
    )

    validate = PythonOperator(
        task_id="validate_data",
        python_callable=validate_ctd_data,
    )

    load_db = PythonOperator(
        task_id="load_to_timescaledb",
        python_callable=load_to_timescaledb,
    )

    report = PythonOperator(
        task_id="generate_report",
        python_callable=generate_summary_report,
    )

    fetch_data >> validate >> load_db >> report
