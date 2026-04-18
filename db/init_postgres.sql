-- Create separate database for Airflow
CREATE DATABASE airflowdb;

-- Enable PostGIS on main db
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    role VARCHAR(50) DEFAULT 'scientist',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Audit log table (append-only)
CREATE TABLE IF NOT EXISTS audit_log (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id),
    action VARCHAR(255) NOT NULL,
    resource VARCHAR(255),
    timestamp TIMESTAMPTZ DEFAULT NOW(),
    details JSONB
);

-- Dataset metadata table
CREATE TABLE IF NOT EXISTS dataset_metadata (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(500) NOT NULL,
    domain VARCHAR(100) NOT NULL,
    file_path VARCHAR(1000),
    file_format VARCHAR(50),
    uploaded_by UUID REFERENCES users(id),
    access_level VARCHAR(50) DEFAULT 'private',
    darwin_core_compliant BOOLEAN DEFAULT FALSE,
    cf_compliant BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    metadata JSONB
);

-- Species table (WoRMS mirror)
CREATE TABLE IF NOT EXISTS species (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    worms_id INTEGER UNIQUE,
    scientific_name VARCHAR(500) NOT NULL,
    kingdom VARCHAR(100),
    phylum VARCHAR(100),
    class VARCHAR(100),
    "order" VARCHAR(100),
    family VARCHAR(100),
    genus VARCHAR(100),
    synonyms JSONB,
    last_synced TIMESTAMPTZ DEFAULT NOW()
);

-- Fisheries survey records
CREATE TABLE IF NOT EXISTS fish_abundance_records (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    survey_id VARCHAR(100),
    species_id UUID REFERENCES species(id),
    worms_id INTEGER,
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    survey_date DATE,
    gear_type VARCHAR(100),
    haul_duration_hours DOUBLE PRECISION,
    cpue_kg_per_hour DOUBLE PRECISION,
    total_weight_kg DOUBLE PRECISION,
    total_count INTEGER,
    station_id VARCHAR(100),
    cruise_id VARCHAR(100),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    raw_data JSONB
);

-- Otolith specimen records
CREATE TABLE IF NOT EXISTS otolith_records (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    specimen_id VARCHAR(100) UNIQUE NOT NULL,
    species_id UUID REFERENCES species(id),
    worms_id INTEGER,
    image_path VARCHAR(1000),
    age_manual INTEGER,
    age_cnn INTEGER,
    age_confidence DOUBLE PRECISION,
    age_class VARCHAR(50),
    validated_by UUID REFERENCES users(id),
    cnn_model_version VARCHAR(100),
    efd_features JSONB,
    morphometric_data JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- eDNA samples table
CREATE TABLE IF NOT EXISTS edna_samples (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    sample_id VARCHAR(100) UNIQUE NOT NULL,
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    depth_m DOUBLE PRECISION,
    collection_date DATE,
    fastq_path VARCHAR(1000),
    primer_set VARCHAR(200),
    target_gene VARCHAR(100),
    sequencing_platform VARCHAR(100),
    pipeline_status VARCHAR(50) DEFAULT 'pending',
    job_id VARCHAR(200),
    mixs_metadata JSONB,
    pipeline_results JSONB,
    diversity_metrics JSONB,
    species_detections JSONB,
    darwin_core_export_path VARCHAR(1000),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Schema matching history
CREATE TABLE IF NOT EXISTS schema_match_log (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    dataset_id UUID REFERENCES dataset_metadata(id),
    source_column VARCHAR(500),
    target_column VARCHAR(500),
    confidence DOUBLE PRECISION,
    auto_applied BOOLEAN DEFAULT FALSE,
    user_confirmed BOOLEAN,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Anomaly detection log
CREATE TABLE IF NOT EXISTS anomaly_log (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    dataset_id UUID REFERENCES dataset_metadata(id),
    row_index INTEGER,
    anomaly_score DOUBLE PRECISION,
    reason VARCHAR(500),
    auto_corrected BOOLEAN DEFAULT FALSE,
    correction_applied VARCHAR(500),
    reviewed_by UUID REFERENCES users(id),
    created_at TIMESTAMPTZ DEFAULT NOW()
);
