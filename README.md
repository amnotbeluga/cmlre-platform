# CMLRE AI-Driven Marine Data Platform

This platform integrates four scientific data domains (Oceanographic, Fisheries, Taxonomy/Otolith, eDNA) with AI-powered data processing, served through a React frontend and FastAPI backends, all orchestrated with Docker Compose.

## How to Start Everything Locally

Run these commands in order from the project root:

```bash
# Step 1: Build all images
docker compose build

# Step 2: Start databases and infrastructure first
docker compose up -d timescaledb mongodb redis minio zookeeper kafka

# Step 3: Wait 30 seconds for databases to be ready, then start services
sleep 30
docker compose up -d ingestion-service ai-layer-service oceanographic-service fisheries-service taxonomy-service molecular-service analytics-service

# Step 4: Start Airflow
docker compose up -d airflow-webserver airflow-scheduler airflow-worker

# Step 5: Start gateway and frontend
docker compose up -d kong frontend

# Step 6: Verify all containers are running
docker compose ps
```
