import os
import asyncio
import asyncpg

# Configuración de la base de datos
db_user = os.getenv("POSTGRES_USER", "postgres")
db_password = os.getenv("POSTGRES_PASSWORD", "123456")
db_host = os.getenv("POSTGRES_HOST", "localhost")
db_port = os.getenv("POSTGRES_PORT", "5432")
db_name = os.getenv("POSTGRES_DB", "pagila")

async def create_table():
    conn = None
    try:
        # Conexión a la base de datos
        conn = await asyncpg.connect(
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
            database=db_name
        )
        print("Conexión exitosa a la base de datos.")

        # Crear la tabla telemetry
        create_table_query = """
        CREATE TABLE IF NOT EXISTS telemetry (
            id SERIAL,
            timestamp TIMESTAMPTZ NOT NULL,
            engine_rpm INT NOT NULL,
            engine_temperature INT NOT NULL,
            geom GEOMETRY(POINT, 4326), -- Almacena geometrías en formato EPSG:4326
            PRIMARY KEY (id, timestamp)
        );
        """
        await conn.execute(create_table_query)
        print("Tabla 'telemetry' creada exitosamente.")

        # Convertir en hipertabla de TimescaleDB
        hypertable_query = """
        SELECT create_hypertable('telemetry', 'timestamp', if_not_exists => TRUE);
        """
        await conn.execute(hypertable_query)
        print("Tabla 'telemetry' convertida en hipertabla de TimescaleDB exitosamente.")

    except Exception as e:
        print(f"Error al crear la tabla: {e}")
    finally:
        if conn:
            await conn.close()
            print("Conexión cerrada.")

if __name__ == "__main__":
    asyncio.run(create_table())