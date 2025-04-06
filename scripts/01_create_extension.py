import os
import asyncio
import asyncpg


db_user = os.getenv("POSTGRES_USER", "postgres")
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

        create_extension_query = "CREATE EXTENSION IF NOT EXISTS postgis;"
        await conn.execute(create_extension_query)
        print("Extensión 'postgis' creada exitosamente.")
    except Exception as e:
        print(f"Error al crear la extensión: {e}")
    finally:
        if conn:
            await conn.close()
            print("Conexión cerrada.")

if __name__ == "__main__":
    asyncio.run(create_table())