import psycopg2
import json
import os
from datetime import datetime

# Connection string
# Running this from host or container? Let's use localhost for host, timescaledb for container.
DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_USER = "cmlre"
DB_PASS = "cmlrepassword"
DB_NAME = "cmlredb"

try:
    conn = psycopg2.connect(
        host=DB_HOST,
        # If running from host, it maps to 5433!
        port=5433 if DB_HOST == "localhost" else 5432, 
        user=DB_USER,
        password=DB_PASS,
        dbname=DB_NAME
    )
    conn.autocommit = True
    cursor = conn.cursor()

    # Create tables if they don't exist (in case init_postgres.sql didn't run)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS species (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        worms_id INTEGER UNIQUE,
        scientific_name VARCHAR(500) NOT NULL,
        kingdom VARCHAR(100),
        phylum VARCHAR(100),
        class VARCHAR(100),
        "order" VARCHAR(100),
        family VARCHAR(100),
        genus VARCHAR(100),
        image_url VARCHAR(500),
        description TEXT,
        status VARCHAR(50)
    );
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS fish_abundance_records (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        station_id VARCHAR(100),
        gear_type VARCHAR(100),
        total_weight_kg DOUBLE PRECISION
    );
    """)

    print("Connected to database. Seeding data...")

    # Seed Species (Taxonomy)
    species_data = [
        (104, 'Aequorea victoria', 'Animalia', 'Cnidaria', 'Scyphozoa', 'Leptothecata', 'Aequoreidae', 'Aequorea', 'Verified', '/assets/jellyfish.png', 'Bioluminescent hydrozoan jellyfish found off the west coast of North America.'),
        (211, 'Acropora cervicornis', 'Animalia', 'Cnidaria', 'Anthozoa', 'Scleractinia', 'Acroporidae', 'Acropora', 'Endangered', '/assets/coral.png', 'Branching, stony coral with cylindrical branches ranging from a few centimeters to over two meters in length.'),
        (893, 'Chaetoceros sp.', 'Chromista', 'Bacillariophyta', 'Bacillariophyceae', 'Chaetocerotales', 'Chaetocerotaceae', 'Chaetoceros', 'Verified', '/assets/plankton.png', 'Microscopic phytoplankton characterized by their distinct silica cell walls (frustules).')
    ]
    
    # We alter the species table slightly to hold image_url and description just for this demo, or put them in JSONB synonyms.
    cursor.execute("ALTER TABLE species ADD COLUMN IF NOT EXISTS image_url VARCHAR(500);")
    cursor.execute("ALTER TABLE species ADD COLUMN IF NOT EXISTS description TEXT;")
    cursor.execute("ALTER TABLE species ADD COLUMN IF NOT EXISTS status VARCHAR(50);")

    cursor.execute("TRUNCATE TABLE species CASCADE;")
    
    for s in species_data:
        cursor.execute("""
            INSERT INTO species (worms_id, scientific_name, kingdom, phylum, class, "order", family, genus, status, image_url, description)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, s)

    print("Species seeded.")

    # Seed Fisheries CPUE (fish_abundance_records)
    cursor.execute("TRUNCATE TABLE fish_abundance_records CASCADE;")
    
    fisheries_data = [
        ('Zone A', 'Sardines', 4000), ('Zone A', 'Mackerel', 2400), ('Zone A', 'Tuna', 2400),
        ('Zone B', 'Sardines', 3000), ('Zone B', 'Mackerel', 1398), ('Zone B', 'Tuna', 2210),
        ('Zone C', 'Sardines', 2000), ('Zone C', 'Mackerel', 9800), ('Zone C', 'Tuna', 2290),
    ]

    for f in fisheries_data:
        # We put species in gear_type and zone in station_id just for quick mapping without complex joins
        cursor.execute("""
            INSERT INTO fish_abundance_records (station_id, gear_type, total_weight_kg)
            VALUES (%s, %s, %s)
        """, (f[0], f[1], f[2]))
        
    print("Fisheries seeded.")

    print("Database seeding complete!")
    
except Exception as e:
    print(f"Error: {e}")
finally:
    if 'conn' in locals():
        conn.close()
