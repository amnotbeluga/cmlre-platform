# CMLRE AI-Driven Unified Marine Data Platform — Technical Walkthrough

> A full-stack microservices platform for ingesting, storing, analyzing, and visualizing marine research data — from oceanographic CTD casts to eDNA bioinformatics.

---

## Table of Contents

1. [Architecture Overview](#1-architecture-overview)
2. [Infrastructure & Deployment](#2-infrastructure--deployment)
3. [Frontend (React + Vite)](#3-frontend-react--vite)
4. [Backend Microservices (FastAPI)](#4-backend-microservices-fastapi)
5. [API Gateway (Kong)](#5-api-gateway-kong)
6. [Databases](#6-databases)
7. [ETL Pipelines (Apache Airflow)](#7-etl-pipelines-apache-airflow)
8. [Data Flow: End-to-End](#8-data-flow-end-to-end)
9. [Running Locally](#9-running-locally)

---

## 1. Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                         BROWSER (:3000)                             │
│                 React + Vite + Recharts + Leaflet                   │
└─────────────────────────┬───────────────────────────────────────────┘
                          │ HTTP (Axios)
                          ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      KONG API GATEWAY (:8000)                       │
│         Rate Limiting · CORS · Route Multiplexing                   │
└──┬──────┬──────┬──────┬──────┬──────┬──────┬────────────────────────┘
   │      │      │      │      │      │      │
   ▼      ▼      ▼      ▼      ▼      ▼      ▼
┌──────┐┌──────┐┌──────┐┌──────┐┌──────┐┌──────┐┌──────┐
│Ingest││  AI  ││Ocean ││Fish  ││Taxon ││Molec ││Analy │
│:8001 ││:8002 ││:8003 ││:8004 ││:8005 ││:8006 ││:8007 │
└──┬───┘└──────┘└──┬───┘└──┬───┘└──┬───┘└──────┘└──────┘
   │               │       │       │
   ▼               ▼       ▼       ▼
┌─────────────────────────────────────────────────────────┐
│              TimescaleDB / PostgreSQL (:5433)            │
│              MongoDB (:27017) · Redis (:6379)            │
│              MinIO (:9000) · Kafka (:9092)               │
└─────────────────────────────────────────────────────────┘
                          ▲
                          │
┌─────────────────────────┴───────────────────────────────┐
│               APACHE AIRFLOW (:8080)                     │
│    3 DAGs: Oceanographic · Fisheries · eDNA              │
└─────────────────────────────────────────────────────────┘
```

The platform follows a **microservices architecture** where each scientific domain (Oceanographic, Fisheries, Taxonomy, Molecular, Analytics) is an independent FastAPI service with its own Docker container, requirements, and API routes. All traffic flows through a Kong API Gateway.

---

## 2. Infrastructure & Deployment

### `docker-compose.yml` — 18 Containers

The entire platform is defined in a single Compose file orchestrating:

| Category | Containers | Purpose |
|----------|-----------|---------|
| **Databases** | `timescaledb`, `mongodb`, `redis` | Time-series, documents, caching |
| **Object Storage** | `minio` | S3-compatible file storage for uploads |
| **Event Streaming** | `zookeeper`, `kafka` | Real-time data event bus |
| **Microservices** | 7 FastAPI containers | Domain-specific business logic |
| **ETL** | `airflow-webserver`, `airflow-scheduler`, `airflow-worker` | Pipeline orchestration |
| **Frontend** | `frontend` | React SPA (Vite dev server) |
| **Gateway** | `kong` | API routing, rate limiting, CORS |

**Key design decisions:**

- All images are explicitly prefixed with `docker.io/` to avoid Podman's interactive registry prompt on Fedora/Bazzite
- Volume mounts use the `:z` SELinux flag (e.g., `./services/oceanographic:/app:z`) to allow container read/write access on SELinux-enforcing systems
- The `depends_on` blocks were removed because `podman-compose` v1.x has a deadlock bug in its `check_dep_conditions` code
- TimescaleDB is mapped to host port `5433` (not `5432`) to avoid conflict with any local PostgreSQL

### `.env` — Environment Variables

All credentials (Postgres, MongoDB, MinIO, Airflow) are centralized in `.env` and injected via `env_file: .env` in each service definition.

---

## 3. Frontend (React + Vite)

### Design System — `src/index.css`

The global CSS establishes a premium dark-mode aesthetic with an ocean-themed color palette:

```css
:root {
  --bg-primary: #0a0e17;      /* Deep ocean black */
  --bg-secondary: #131b2c;    /* Dark panel background */
  --accent-primary: #0ea5e9;  /* Cyan — primary brand */
  --accent-secondary: #8b5cf6; /* Violet — secondary accent */
  --glass-bg: rgba(19, 27, 44, 0.7);  /* Glassmorphism panels */
  --glass-border: rgba(255, 255, 255, 0.08);
}
```

The `.glass-panel` class provides the glassmorphism effect used on every card and sidebar:
```css
.glass-panel {
  background: var(--glass-bg);
  backdrop-filter: blur(12px);
  border: 1px solid var(--glass-border);
  border-radius: 16px;
  box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.2);
}
```

Ambient background glows are achieved via two subtle radial gradients on the `<body>`.

### Layout — `src/components/Layout.tsx`

The app shell uses a fixed glassmorphism sidebar with React Router navigation. Active routes get a cyan glow border. The sidebar includes:
- Navigation links with emoji icons
- A user avatar section at the bottom
- Active route highlighting via `useLocation()`

### Routing — `src/App.tsx`

```tsx
<BrowserRouter>
  <Layout>
    <Routes>
      <Route path="/" element={<Dashboard />} />
      <Route path="/oceanographic" element={<Oceanographic />} />
      <Route path="/fisheries" element={<Fisheries />} />
      <Route path="/taxonomy" element={<Taxonomy />} />
      <Route path="/molecular" element={<Molecular />} />
      <Route path="/analytics" element={<Analytics />} />
    </Routes>
  </Layout>
</BrowserRouter>
```

### API Client — `src/api/client.ts`

A centralized Axios client handles all backend communication:

```typescript
const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

export const apiClient = axios.create({
  baseURL: API_BASE,   // Points to Kong Gateway
  timeout: 30000,
});
```

An interceptor automatically attaches JWT tokens from `localStorage` to every request header. The `api` object exposes typed methods for every endpoint:

| Method | Endpoint | Service |
|--------|----------|---------|
| `api.getStations()` | `GET /api/v1/oceanography/stations` | Oceanographic |
| `api.getCPUE()` | `GET /api/v1/fisheries/cpue` | Fisheries |
| `api.getSpecies()` | `GET /api/v1/taxonomy/species` | Taxonomy |
| `api.getEDNAComposition()` | `GET /api/v1/molecular/edna/composition` | Molecular |
| `api.getDepthProfile()` | `GET /api/v1/analytics/depth-profile` | Analytics |
| `api.runCorrelation()` | `POST /api/v1/analytics/correlation` | Analytics |
| `api.semanticSearch()` | `GET /api/v1/ai/search` | AI Layer |
| ...and 12 more | | |

### Pages

#### Dashboard (`pages/Dashboard.tsx`)
- 4 KPI stat cards (Total Stations, Active Sensors, Species Catalogued, eDNA Samples)
- Recharts `<AreaChart>` showing monthly SST from the Arabian Sea
- Gradient fills and glassmorphism card styling

#### Oceanographic (`pages/Oceanographic.tsx`)
- `react-leaflet` `<MapContainer>` with dark Stadia tiles
- `<CircleMarker>` for each sensor station — color-coded by temperature
- Click a marker → telemetry sidebar updates with station metadata
- Data fetched from `api.getStations()` via `useEffect`

#### Fisheries (`pages/Fisheries.tsx`)
- Recharts stacked `<BarChart>` showing CPUE (Sardines, Mackerel, Tuna) by zone
- Data table for recent vessel activity logs
- CPUE data fetched from `api.getCPUE()`

#### Taxonomy (`pages/Taxonomy.tsx`)
- Image gallery grid with AI-generated specimen photos (coral, jellyfish, plankton)
- Cards show phylum → class hierarchy, status badges (Verified/Endangered)
- Data fetched from `api.getSpecies()` which queries PostgreSQL

#### Molecular / eDNA (`pages/Molecular.tsx`)
- **Genome Sequence Viewer** — monospace ATCG rendering with nucleotide color-coding (A=red, T=blue, C=green, G=yellow)
- GC content badge computed from backend
- Recharts `<PieChart>` for taxonomic composition (donut chart)
- Sample selector pills — switch between eDNA samples
- Metadata sidebar showing collection date, depth, filter type, Shannon Index
- All data fetched from 3 parallel API calls: `getEDNAComposition()`, `getEDNASequence()`, `getEDNASamples()`

#### Analytics (`pages/Analytics.tsx`)
- Recharts `<ScatterChart>` — Temperature vs Depth (bubble size = salinity)
- Recharts `<LineChart>` — SST Anomaly trend (2015–2024), red "High Alert" badge
- **Interactive correlation button** — calls `api.runCorrelation()` and displays r, p-value, R², method, and interpretation inline
- Data fetched from `getDepthProfile()` and `getSSTAnomaly()`

---

## 4. Backend Microservices (FastAPI)

Each service follows the same pattern:

```
services/<name>/
├── main.py          # FastAPI app, CORS middleware, router registration
├── routers/         # Endpoint modules
├── requirements.txt # Python dependencies
└── Dockerfile       # python:3.11-slim + pip install + uvicorn --reload
```

### 4.1 Ingestion Service (`:8001`)

**File:** `services/ingestion/routers/upload.py`

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/ingest/upload` | POST | Accept file uploads, detect format from extension |
| `/api/v1/ingest/uploads` | GET | Return upload history |
| `/api/v1/ingest/formats` | GET | List supported formats |

**How it works:** When a file is uploaded, the extension is matched against a `FORMAT_MAP` dictionary mapping `.csv` → `tabular_ingest`, `.nc` → `oceanographic_ingest`, `.fasta` → `molecular_ingest`, etc. Each upload gets a UUID, is logged in an in-memory registry, and returns the detected format + target pipeline.

### 4.2 AI Layer Service (`:8002`)

**File:** `services/ai_layer/routers/ai.py`

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/ai/search` | GET | Keyword search across all platform datasets |
| `/api/v1/ai/schema-match` | POST | Map CSV column headers to known field types |

**How search works:** A `KNOWLEDGE_BASE` list contains 17 items spanning stations, species, fisheries zones, eDNA samples, and analytical concepts. Each item has tags. The `_score_result()` function scores items by:
- +10 points for title match
- +5 points for tag match
- +2 points for description match

Results are sorted by score and returned.

### 4.3 Oceanographic Service (`:8003`)

**Files:** `routers/stations.py`, `routers/profiles.py`, `routers/climatology.py`

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/oceanography/stations` | GET | All monitoring stations with telemetry |
| `/api/v1/oceanography/profiles` | GET | Summary list of available CTD casts |
| `/api/v1/oceanography/profiles/{id}` | GET | Full CTD vertical profile (14 depth layers) |
| `/api/v1/oceanography/climatology` | GET | Monthly climatological means (SST, salinity, wind) |
| `/api/v1/oceanography/climatology/regions` | GET | Available sub-regions (Arabian Sea, Bay of Bengal, etc.) |
| `/api/v1/oceanography/climatology/{region}` | GET | Regional climatology data |

**CTD Profile data** includes temperature, salinity, dissolved oxygen, and chlorophyll at each depth layer — modeled after real CTD cast data from Indian Ocean research cruises.

### 4.4 Fisheries Service (`:8004`)

**Files:** `routers/cpue.py`, `routers/abundance.py`

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/fisheries/cpue` | GET | CPUE by zone (Sardines, Mackerel, Tuna) |
| `/api/v1/fisheries/abundance` | GET | Fish abundance survey records |
| `/api/v1/fisheries/abundance/summary` | GET | Aggregate statistics (total biomass, surveys) |

Each abundance record contains `surveyId`, `zone`, `gearType`, `speciesCount`, `totalBiomassKg`, `dominantSpecies`, and `shannonDiversity`.

### 4.5 Taxonomy Service (`:8005`)

**Files:** `routers/species.py`, `routers/otolith.py`, `routers/vouchers.py`

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/taxonomy/species` | GET | Query PostgreSQL for catalogued species |
| `/api/v1/taxonomy/otolith/analyze` | POST | CV-based otolith age/species analysis |
| `/api/v1/taxonomy/otolith/models` | GET | Available ML models |
| `/api/v1/taxonomy/vouchers` | GET | All voucher specimens |
| `/api/v1/taxonomy/vouchers/{id}` | GET | Single voucher detail |
| `/api/v1/taxonomy/vouchers/stats` | GET | Collection statistics |

**`species.py`** is the only service that connects to PostgreSQL via `psycopg2`. It queries the `species` table seeded by `seed_db.py`.

**`otolith.py`** simulates computer vision analysis of fish ear bone images. When an image is uploaded, it returns mock predictions: species identification with confidence scores, estimated age from growth rings, and morphometric measurements (length, width, area, circularity).

**`vouchers.py`** manages physical specimen records with preservation details, DNA extraction status, GenBank accession numbers, and morphometric data.

### 4.6 Molecular / eDNA Service (`:8006`)

**Files:** `routers/edna.py`, `routers/pipeline.py`

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/molecular/edna/composition` | GET | Taxonomic composition breakdown |
| `/api/v1/molecular/edna/samples` | GET | All processed eDNA samples |
| `/api/v1/molecular/edna/submit` | POST | Submit new sample for processing |
| `/api/v1/molecular/edna/{id}/results` | GET | Results for specific sample |
| `/api/v1/molecular/edna/sequence` | GET | Random ATCG sequence + GC content |
| `/api/v1/molecular/pipeline/status` | GET | Bioinformatics pipeline stages |
| `/api/v1/molecular/pipeline/runs` | GET | Recent pipeline run history |

**Sequence generation:** `_generate_sequence()` produces random DNA sequences. The GC content (percentage of G+C bases) is computed server-side and returned alongside the sequence.

**Pipeline stages** model a real metabarcoding workflow: FastQC → Cutadapt → DADA2 → BLAST → MAFFT, each with duration and read count metrics.

### 4.7 Analytics Service (`:8007`)

**File:** `routers/correlation.py`

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/analytics/correlation` | POST | Pearson correlation between variables |
| `/api/v1/analytics/depth-profile` | GET | Temperature/salinity vs depth |
| `/api/v1/analytics/sst-anomaly` | GET | SST anomaly time-series (2015–2024) |
| `/api/v1/analytics/summary` | GET | High-level platform statistics |

The **correlation endpoint** accepts `variableX` and `variableY` parameters and returns `correlationCoefficient`, `pValue`, `rSquared`, `method`, and a human-readable `interpretation` string.

---

## 5. API Gateway (Kong)

**File:** `gateway/kong.yml`

Kong runs in declarative (DB-less) mode. The config maps URL prefixes to internal service containers:

```yaml
services:
  - name: oceanographic-service
    url: http://oceanographic-service:8003
    routes:
      - paths: ["/api/v1/oceanography"]
        strip_path: false
```

Global plugins apply rate limiting (1000 req/min) and CORS (allowing `http://localhost:3000`).

---

## 6. Databases

### TimescaleDB (PostgreSQL)

**Connection:** `timescaledb:5432` (internal) / `localhost:5433` (host)

Tables seeded by `services/ingestion/seed_db.py`:

| Table | Purpose |
|-------|---------|
| `species` | Taxonomic catalogue (worms_id, scientific_name, phylum, class, etc.) |
| `fish_abundance_records` | Fisheries survey records |
| `ctd_observations` | Created by Airflow DAG for time-series CTD data |
| `fisheries_daily_summary` | Created by Airflow DAG for daily CPUE aggregates |

### MongoDB

Used for unstructured document storage (raw data files, metadata).

### Redis

Available for caching and session management.

### MinIO

S3-compatible object storage for uploaded files (CSV, NetCDF, FASTA).

---

## 7. ETL Pipelines (Apache Airflow)

Three DAGs in `airflow/dags/`:

### 7.1 `oceanographic_ingestion.py`

**Schedule:** Every 6 hours

```
fetch_station_data → validate_data → load_to_timescaledb → generate_report
```

1. **Fetch** — `SimpleHttpOperator` calls the Oceanographic service's `/stations` endpoint
2. **Validate** — QC checks: temperature must be -2°C to 35°C, salinity must be 0–42 PSU. Failed records are logged and rejected
3. **Load** — Validated records are inserted into the `ctd_observations` table in TimescaleDB
4. **Report** — Summary with pass/reject counts pushed to XCom

### 7.2 `fisheries_cpue_ingestion.py`

**Schedule:** Daily at 02:00 UTC

```
┌─ fetch_cpue ──┐
│               ├──→ compute_aggregates → store_aggregates
└─ fetch_abundance ┘
```

1. **Fetch** — Two parallel Python tasks call the Fisheries service for CPUE and abundance data
2. **Aggregate** — Computes total catch per species across all zones + total biomass
3. **Store** — Upserts a daily summary row into `fisheries_daily_summary` (uses `ON CONFLICT DO UPDATE`)

### 7.3 `edna_bioinformatics.py`

**Schedule:** Every 12 hours

```
check_samples ──→ [run_pipeline] → store_composition → biodiversity_report
              └──→ [no_new_samples]
```

1. **Check** — `BranchPythonOperator` queries the Molecular service for pending samples. If none found, the DAG short-circuits
2. **Pipeline** — Simulates the 5-stage bioinformatics workflow (FastQC → Cutadapt → DADA2 → BLAST → MAFFT)
3. **Store** — Fetches taxonomic composition and pushes to XCom
4. **Report** — Generates a biodiversity summary with Shannon Diversity Index and dominant taxon

---

## 8. Data Flow: End-to-End

Here's how a piece of data flows through the entire system:

```
1. Scientist uploads a CSV file
   └─→ Frontend (React) sends POST to /api/v1/ingest/upload

2. Kong Gateway routes to Ingestion Service (:8001)
   └─→ Format detected as CSV, queued for tabular_ingest pipeline

3. Airflow DAG (scheduled or triggered) picks up the job
   └─→ Fetches data from the relevant microservice
   └─→ Validates (QC checks)
   └─→ Loads into TimescaleDB

4. Frontend page (e.g., Oceanographic) calls GET /api/v1/oceanography/stations
   └─→ Kong routes to Oceanographic Service (:8003)
   └─→ Service returns JSON data
   └─→ React renders it on a Leaflet map with Recharts graphs
```

---

## 9. Running Locally

### Prerequisites
- Podman (or Docker) with compose support
- ~8GB disk space for container images

### Start Everything
```bash
cd /home/levi/Documents/cmlre-platform
source .venv/bin/activate
podman-compose up -d --build
```

### Seed the Database
```bash
podman exec cmlre-ingestion python /app/seed_db.py
```

### Access Points

| Service | URL |
|---------|-----|
| **Frontend** | http://localhost:3000 |
| **API Gateway** | http://localhost:8000 |
| **Airflow Dashboard** | http://localhost:8080 |
| **MinIO Console** | http://localhost:9001 |

### Useful Commands
```bash
# Check container status
podman-compose ps

# View service logs
podman logs cmlre-frontend
podman logs cmlre-oceanographic

# Stop everything
podman-compose down

# Rebuild a single service
podman-compose up -d --build oceanographic-service
```

---

## Project Structure

```
cmlre-platform/
├── .env                          # All credentials
├── docker-compose.yml            # 18-container orchestration
├── gateway/
│   └── kong.yml                  # API Gateway route config
├── db/
│   ├── init_postgres.sql         # PostgreSQL schema init
│   ├── init_timescale.sql        # TimescaleDB extensions
│   └── init_mongo.js             # MongoDB collections
├── airflow/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── dags/
│       ├── oceanographic_ingestion.py
│       ├── fisheries_cpue_ingestion.py
│       └── edna_bioinformatics.py
├── frontend/
│   ├── index.html
│   ├── vite.config.ts
│   ├── package.json
│   └── src/
│       ├── main.tsx              # React entry point
│       ├── index.css             # Global design system
│       ├── App.tsx               # Router setup
│       ├── api/client.ts         # Axios API client (32 endpoints)
│       ├── components/
│       │   └── Layout.tsx        # Glassmorphism sidebar shell
│       └── pages/
│           ├── Dashboard.tsx     # KPI cards + SST chart
│           ├── Oceanographic.tsx # Leaflet map + sensors
│           ├── Fisheries.tsx     # CPUE bar chart + data table
│           ├── Taxonomy.tsx      # Specimen gallery (PostgreSQL)
│           ├── Molecular.tsx     # eDNA sequence viewer + pie chart
│           └── Analytics.tsx     # Scatter/line charts + correlation
└── services/
    ├── ingestion/                # File upload + format detection
    ├── ai_layer/                 # Semantic search + schema matching
    ├── oceanographic/            # Stations, CTD profiles, climatology
    ├── fisheries/                # CPUE, abundance surveys
    ├── taxonomy/                 # Species DB, otolith CV, vouchers
    ├── molecular/                # eDNA composition, pipeline, sequences
    └── analytics/                # Correlation, depth profiles, SST anomaly
```

---

*Built with FastAPI · React · Vite · Recharts · Leaflet · TimescaleDB · MongoDB · Redis · MinIO · Kafka · Kong · Apache Airflow · Podman*
