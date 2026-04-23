CREATE EXTENSION IF NOT EXISTS timescaledb;

CREATE TABLE IF NOT EXISTS ctd_measurements (
    id UUID DEFAULT uuid_generate_v4(),
    cruise_id VARCHAR(100) NOT NULL,
    station_id VARCHAR(100) NOT NULL,
    latitude DOUBLE PRECISION NOT NULL,
    longitude DOUBLE PRECISION NOT NULL,
    timestamp TIMESTAMPTZ NOT NULL,
    depth_m DOUBLE PRECISION NOT NULL,
    temperature_c DOUBLE PRECISION,
    salinity_psu DOUBLE PRECISION,
    dissolved_oxygen_mgL DOUBLE PRECISION,
    fluorescence_ugL DOUBLE PRECISION,
    pressure_dbar DOUBLE PRECISION,
    quality_flag INTEGER DEFAULT 0,
    anomaly_score DOUBLE PRECISION,
    dataset_id UUID,
    PRIMARY KEY (id, timestamp)
);

SELECT create_hypertable(
    'ctd_measurements',
    'timestamp',
    partitioning_column => 'cruise_id',
    number_partitions => 4,
    if_not_exists => TRUE
);

CREATE INDEX IF NOT EXISTS idx_ctd_cruise ON ctd_measurements(cruise_id, timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_ctd_station ON ctd_measurements(station_id, timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_ctd_location ON ctd_measurements(latitude, longitude);

CREATE MATERIALIZED VIEW IF NOT EXISTS ctd_climatology AS
SELECT
    station_id,
    EXTRACT(MONTH FROM timestamp) AS month,
    ROUND(latitude::numeric, 1) AS lat_grid,
    ROUND(longitude::numeric, 1) AS lon_grid,
    AVG(temperature_c) AS avg_temperature,
    AVG(salinity_psu) AS avg_salinity,
    AVG(dissolved_oxygen_mgL) AS avg_do,
    AVG(fluorescence_ugL) AS avg_fluorescence,
    COUNT(*) AS record_count
FROM ctd_measurements
WHERE quality_flag = 0
GROUP BY station_id, month, lat_grid, lon_grid;
