import os
import json
import asyncio
import asyncpg
from shapely.geometry import shape

# Configuración de la base de datos
db_user = os.getenv("POSTGRES_USER", "postgres")
db_password = os.getenv("POSTGRES_PASSWORD", "123456")
db_host = os.getenv("POSTGRES_HOST", "localhost")
db_port = os.getenv("POSTGRES_PORT", "5432")
db_name = os.getenv("POSTGRES_DB", "pagila")

async def load_telemetry():
    conn = None
    try:
        # Leer el archivo JSON
        with open("telemetry.json", "r") as file:
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
                INSERT INTO telemetry (engine_rpm, engine_temperature, geom)
                VALUES ($1, $2, ST_GeomFromText($3, 4326))
                """,
                properties.get("engine_rpm"),
                properties.get("engine_temperature"),
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
    asyncio.run(load_telemetry())