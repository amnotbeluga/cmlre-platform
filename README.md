# 🌊 CMLRE AI-Driven Unified Marine Data Platform

<div align="center">

**An enterprise-grade, full-stack platform for integrating, analyzing, and visualizing multi-domain marine scientific data — built for the Centre for Marine Living Resources and Ecology (CMLRE).**

[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)](https://react.dev)
[![TimescaleDB](https://img.shields.io/badge/TimescaleDB-FDB515?style=for-the-badge&logo=timescale&logoColor=black)](https://www.timescale.com)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com)
[![Apache Airflow](https://img.shields.io/badge/Airflow-017CEE?style=for-the-badge&logo=apacheairflow&logoColor=white)](https://airflow.apache.org)
[![Kong](https://img.shields.io/badge/Kong-003459?style=for-the-badge&logo=kong&logoColor=white)](https://konghq.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](./LICENSE)

</div>

---

## 📋 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Microservices](#microservices)
- [ETL Pipelines](#etl-pipelines)
- [Database Schema](#database-schema)
- [Getting Started](#getting-started)
- [Service Endpoints](#service-endpoints)
- [Frontend Modules](#frontend-modules)

---

## Overview

This platform unifies **four scientific data domains** into a single cohesive system with AI-powered data processing:

| Domain | Description |
|--------|-------------|
| **Oceanographic** | CTD sensor telemetry, sea surface temperature monitoring, salinity profiles, and climatological baselines across the Arabian Sea & Bay of Bengal |
| **Fisheries** | Catch Per Unit Effort (CPUE) analysis, species abundance surveys, vessel logs, and biomass assessments across Indian coastal zones |
| **Taxonomy & Otolith** | WoRMS-integrated species classification, CNN-based otolith age estimation, voucher specimen management, and morphometric analysis |
| **Molecular / eDNA** | Environmental DNA sample processing, metabarcoding pipelines (FastQC → Cutadapt → DADA2 → BLAST → MAFFT), biodiversity reporting |

The platform additionally provides:
- **AI Layer** — Semantic search across all domains, automated schema matching for heterogeneous datasets
- **Analytics Engine** — Depth-profile correlations, SST anomaly trend analysis, Pearson statistical modeling
- **Data Ingestion** — Multi-format file upload (CSV, NetCDF, FASTA, FASTQ, GeoJSON, Excel) with automatic pipeline routing

---

## Architecture

```
                          ┌─────────────┐
                          │   Frontend   │
                          │  React/Vite  │
                          │   :3000      │
                          └──────┬───────┘
                                 │
                          ┌──────▼───────┐
                          │  Kong API    │
                          │  Gateway     │
                          │   :8000      │
                          └──────┬───────┘
                                 │
            ┌────────────────────┼────────────────────┐
            │                    │                     │
   ┌────────▼─────┐   ┌────────▼─────┐    ┌─────────▼────────┐
   │  Ingestion   │   │Oceanographic │    │    Fisheries     │
   │   :8001      │   │   :8003      │    │     :8004        │
   └──────────────┘   └──────────────┘    └──────────────────┘
            │                    │                     │
   ┌────────▼─────┐   ┌────────▼─────┐    ┌─────────▼────────┐
   │  AI Layer    │   │  Taxonomy    │    │    Molecular     │
   │   :8002      │   │   :8005      │    │     :8006        │
   └──────────────┘   └──────────────┘    └──────────────────┘
                                 │
                       ┌────────▼─────┐
                       │  Analytics   │
                       │   :8007      │
                       └──────────────┘
                                 │
     ┌───────────────────────────┼───────────────────────────┐
     │                           │                           │
┌────▼──────┐          ┌────────▼─────┐           ┌─────────▼──┐
│TimescaleDB│          │   MongoDB    │           │   Redis    │
│  :5433    │          │   :27017     │           │   :6379    │
└───────────┘          └──────────────┘           └────────────┘
     │                                                    │
┌────▼──────┐          ┌──────────────┐           ┌───────▼────┐
│   MinIO   │          │    Kafka     │           │  Airflow   │
│  :9000    │          │   :9092      │           │   :8080    │
└───────────┘          └──────────────┘           └────────────┘
```

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | React 18, TypeScript, Vite, Recharts, Leaflet, CSS3 (Glassmorphism) |
| **API Gateway** | Kong 3.4 (Declarative mode, rate limiting, CORS) |
| **Backend** | Python 3.11, FastAPI (7 microservices) |
| **Time-Series DB** | TimescaleDB (PostgreSQL 15 + PostGIS + Hypertables) |
| **Document Store** | MongoDB 7.0 (ecomorphology records, pipeline jobs) |
| **Object Storage** | MinIO (S3-compatible, raw file storage) |
| **Message Broker** | Apache Kafka 7.5 (event streaming) |
| **Cache** | Redis 7.2 (Celery broker, session cache) |
| **Orchestration** | Apache Airflow 2.x (CeleryExecutor, 3 DAGs) |
| **Containerization** | Docker Compose v3.9 (20+ containers) |

---

## Project Structure

```
cmlre-platform/
├── frontend/                    React frontend application
│   ├── src/
│   │   ├── api/client.ts        Axios API client with interceptors
│   │   ├── components/
│   │   │   └── Layout.tsx       Sidebar navigation layout
│   │   ├── pages/
│   │   │   ├── Dashboard.tsx    Platform overview with SST trends
│   │   │   ├── Oceanographic.tsx Leaflet map + sensor telemetry
│   │   │   ├── Fisheries.tsx    CPUE charts + vessel log table
│   │   │   ├── Taxonomy.tsx     Species cards with live DB data
│   │   │   ├── Molecular.tsx    eDNA sequence viewer + pie charts
│   │   │   └── Analytics.tsx    Scatter plots + correlation engine
│   │   ├── index.css            Design system (dark glassmorphism)
│   │   └── App.tsx              Router configuration
│   ├── Dockerfile
│   └── vite.config.ts
│
├── services/                    FastAPI microservices
│   ├── ingestion/               File upload + format detection
│   │   ├── routers/upload.py    Multi-format upload endpoint
│   │   ├── main.py
│   │   └── seed_db.py           Database seeding script
│   ├── ai_layer/                Semantic search + schema matching
│   │   └── routers/ai.py       Knowledge base search + column mapping
│   ├── oceanographic/           CTD data service
│   │   └── routers/
│   │       ├── stations.py      Monitoring station data
│   │       ├── profiles.py      Vertical CTD profiles (4 stations)
│   │       └── climatology.py   Monthly climatological averages
│   ├── fisheries/               Catch & abundance service
│   │   └── routers/
│   │       ├── cpue.py          CPUE by zone
│   │       ├── abundance.py     Survey biomass records
│   │       └── surveys.py       Survey listing
│   ├── taxonomy/                Species & specimen service
│   │   └── routers/
│   │       ├── species.py       Live DB query (PostgreSQL)
│   │       ├── otolith.py       CNN-based otolith analysis
│   │       └── vouchers.py      Voucher specimen registry
│   ├── molecular/               eDNA & pipeline service
│   │   └── routers/
│   │       ├── edna.py          Sample management + composition
│   │       └── pipeline.py      Bioinformatics pipeline status
│   └── analytics/               Statistical analysis service
│       └── routers/
│           └── correlation.py   Pearson correlation + depth profiles
│
├── airflow/                     ETL orchestration
│   └── dags/
│       ├── oceanographic_ingestion.py   CTD → TimescaleDB (6h)
│       ├── fisheries_cpue_ingestion.py  CPUE aggregation (daily)
│       └── edna_bioinformatics.py       eDNA pipeline (12h)
│
├── db/                          Database initialization
│   ├── init_postgres.sql        PostgreSQL schema (9 tables)
│   ├── init_timescale.sql       Hypertable + materialized views
│   └── init_mongo.js            MongoDB collections + validators
│
├── gateway/
│   └── kong.yml                 API gateway routing + plugins
│
├── docker-compose.yml           Full stack orchestration
├── .env                         Environment configuration
└── seed_db.py                   Host-side database seeder
```

---

## Microservices

### Ingestion Service `:8001`
Handles multi-format file upload with automatic format detection. Supports CSV, TSV, NetCDF, FASTA, FASTQ, JSON, Excel, and GeoJSON. Each file is routed to the appropriate processing pipeline based on its extension.

### AI Layer Service `:8002`
Provides semantic search across all data domains (stations, species, fisheries zones, eDNA samples, scientific concepts) using a keyword scoring engine. Also offers automated column-to-schema mapping for heterogeneous dataset integration.

### Oceanographic Service `:8003`
Serves monitoring station data from 4 active buoys (Arabian Sea, Bay of Bengal, Lakshadweep, Andaman). Provides full CTD vertical profiles (surface to 2000m) and monthly climatological baselines for 4 ocean regions.

### Fisheries Service `:8004`
Delivers CPUE data across 6 fishing zones, species abundance survey records from 4 coastal zones (Kerala, Karnataka, Tamil Nadu, Andhra Pradesh), and biomass summaries.

### Taxonomy Service `:8005`
Connects directly to PostgreSQL for live species data. Features CNN-based otolith age estimation (ResNet-50 + EfficientNet-B4 models), morphometric analysis, and a voucher specimen registry with GenBank accession tracking.

### Molecular Service `:8006`
Manages eDNA water samples with full bioinformatics pipeline tracking (FastQC → Cutadapt → DADA2 → BLAST → MAFFT). Provides taxonomic composition breakdowns and synthetic sequence generation for visualization.

### Analytics Service `:8007`
Computes Pearson correlation analysis between oceanographic variables, serves depth-temperature profiles, and tracks SST anomaly trends from 2015–2024.

---

## ETL Pipelines

| DAG | Schedule | Description |
|-----|----------|-------------|
| `oceanographic_data_ingestion` | Every 6 hours | Fetches station data → QC validation (temp/salinity range checks) → TimescaleDB load → summary report |
| `fisheries_cpue_ingestion` | Daily at 02:00 UTC | Fetches CPUE + abundance data → species-level aggregation → stores daily summary to PostgreSQL |
| `edna_bioinformatics_pipeline` | Every 12 hours | Checks for pending samples → runs bioinformatics pipeline → stores taxonomic composition → generates biodiversity report |

---

## Database Schema

### PostgreSQL / TimescaleDB
- `users` — Platform user accounts with role-based access
- `audit_log` — Append-only action audit trail
- `dataset_metadata` — Uploaded dataset catalog (Darwin Core / CF compliance flags)
- `species` — WoRMS-mirrored taxonomic records
- `fish_abundance_records` — Fisheries survey catch data
- `otolith_records` — Specimen age estimation with CNN model tracking
- `edna_samples` — eDNA sample lifecycle (collection → pipeline → results)
- `schema_match_log` — AI-driven column mapping history
- `anomaly_log` — Data quality anomaly detection records
- `ctd_measurements` — TimescaleDB hypertable for oceanographic time-series
- `ctd_climatology` — Materialized view for station-level monthly averages

### MongoDB
- `ecomorphology_records` — Morphometric specimen data with JSON schema validation
- `pipeline_jobs` — Bioinformatics job tracking
- `bert_index_metadata` — NLP model index metadata

---

## Getting Started

### Prerequisites
- Docker & Docker Compose
- 8 GB+ RAM recommended (20+ containers)

### Launch

```bash
docker compose build

docker compose up -d timescaledb mongodb redis minio zookeeper kafka

sleep 30

docker compose up -d ingestion-service ai-layer-service oceanographic-service fisheries-service taxonomy-service molecular-service analytics-service

docker compose up -d airflow-webserver airflow-scheduler airflow-worker

docker compose up -d kong frontend

docker compose ps
```

### Seed the Database

```bash
pip install psycopg2-binary
python seed_db.py
```

---

## Service Endpoints

| Port | Service | URL |
|------|---------|-----|
| 3000 | Frontend | http://localhost:3000 |
| 8000 | Kong API Gateway | http://localhost:8000 |
| 8001 | Ingestion | http://localhost:8001/docs |
| 8002 | AI Layer | http://localhost:8002/docs |
| 8003 | Oceanographic | http://localhost:8003/docs |
| 8004 | Fisheries | http://localhost:8004/docs |
| 8005 | Taxonomy | http://localhost:8005/docs |
| 8006 | Molecular | http://localhost:8006/docs |
| 8007 | Analytics | http://localhost:8007/docs |
| 8080 | Airflow UI | http://localhost:8080 |
| 9001 | MinIO Console | http://localhost:9001 |

### API Routes via Gateway

```
GET  /api/v1/oceanography/stations          Station monitoring data
GET  /api/v1/oceanography/profiles/{id}     CTD vertical profiles
GET  /api/v1/oceanography/climatology       Monthly climate baselines

GET  /api/v1/fisheries/cpue                 CPUE by zone
GET  /api/v1/fisheries/abundance            Survey biomass data
GET  /api/v1/fisheries/abundance/summary    Aggregated statistics

GET  /api/v1/taxonomy/species               Live species from DB
POST /api/v1/taxonomy/otolith/analyze       Otolith image analysis
GET  /api/v1/taxonomy/vouchers              Specimen registry

GET  /api/v1/molecular/edna/samples         eDNA sample listing
GET  /api/v1/molecular/edna/composition     Taxonomic composition
GET  /api/v1/molecular/edna/sequence        Synthetic sequence data
GET  /api/v1/molecular/pipeline/status      Pipeline stage tracking

POST /api/v1/analytics/correlation          Run Pearson correlation
GET  /api/v1/analytics/depth-profile        Depth vs temperature
GET  /api/v1/analytics/sst-anomaly          SST anomaly time-series

GET  /api/v1/ai/search?query={q}           Semantic search
POST /api/v1/ai/schema-match               Column mapping

POST /api/v1/ingest/upload                  File upload
GET  /api/v1/ingest/uploads                 Upload history
GET  /api/v1/ingest/formats                 Supported formats
```

---

## Frontend Modules

| Module | Features |
|--------|----------|
| **Dashboard** | Live statistics, SST & salinity area charts, system health indicators |
| **Oceanographic** | Interactive Leaflet dark map, real-time sensor telemetry panel, station detail cards |
| **Fisheries** | Stacked bar charts (CPUE by zone & species), vessel log table, zone statistics |
| **Taxonomy** | Species image cards with taxonomic hierarchy, status badges, live PostgreSQL data |
| **Molecular** | DNA sequence viewer with color-coded nucleotides, donut chart taxonomic composition, sample metadata panel |
| **Analytics** | Depth-temperature scatter plot, SST anomaly line chart, interactive Pearson correlation engine |

---

<div align="center">

**Centre for Marine Living Resources and Ecology**

Built with ❤️ for marine science

</div>
