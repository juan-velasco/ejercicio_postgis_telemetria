import os
import json
import asyncio
import asyncpg
from shapely.geometry import shape
from geojson import FeatureCollection

# Configuración de la base de datos
db_user = os.getenv("POSTGRES_USER", "postgres")
db_password = os.getenv("POSTGRES_PASSWORD", "123456")
db_host = os.getenv("POSTGRES_HOST", "localhost")
db_port = os.getenv("POSTGRES_PORT", "5432")
db_name = os.getenv("POSTGRES_DB", "pagila")

async def load_countries():
    conn = None
    try:
        # Leer el archivo JSON
        with open("countries.json", "r") as file:
            data = json.load(file)
        
        # Conexión a la base de datos
        conn = await asyncpg.connect(
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
            database=db_name
        )
        print("Conexión exitosa a la base de datos.")

        # Insertar datos en la tabla
        for feature in data["features"]:
            properties = feature["properties"]
            geometry = shape(feature["geometry"])  # Convertir a objeto Shapely
            wkt_geometry = geometry.wkt  # Convertir a WKT (Well-Known Text)

            # Insertar en la tabla
            await conn.execute(
                """
                INSERT INTO countries (name, iso2, iso3, population, region, subregion, geom)
                VALUES ($1, $2, $3, $4, $5, $6, ST_GeomFromText($7, 4326))
                """,
                properties.get("NAME"),
                properties.get("ISO2"),
                properties.get("ISO3"),
                properties.get("POP2005"),
                properties.get("REGION"),
                properties.get("SUBREGION"),
                wkt_geometry
            )
        print("Datos insertados exitosamente.")
    except Exception as e:
        print(f"Error al cargar los datos: {e}")
    finally:
        if conn:
            await conn.close()
            print("Conexión cerrada.")

if __name__ == "__main__":
    asyncio.run(load_countries())