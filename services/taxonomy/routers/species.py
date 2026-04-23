from fastapi import APIRouter
import psycopg2
import os

router = APIRouter()

DB_HOST = os.getenv("POSTGRES_HOST", "timescaledb")

def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=5432,
        user="cmlre",
        password="cmlrepassword",
        dbname="cmlredb"
    )

@router.get("/species")
async def get_species():
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT worms_id, scientific_name, phylum, class, status, image_url, description FROM species")
        rows = cursor.fetchall()
        
        result = []
        for row in rows:
            result.append({
                "id": f"TAX-{row[0]}",
                "phylum": row[2],
                "class": row[3],
                "species": row[1],
                "commonName": row[1],
                "description": row[6],
                "imageUrl": row[5],
                "status": row[4]
            })
        return result
    except Exception as e:
        return {"error": str(e)}
    finally:
        if conn is not None:
            conn.close()
