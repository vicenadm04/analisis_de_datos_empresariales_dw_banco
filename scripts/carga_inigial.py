import psycopg2
from config import DB_URI
from init_db import init_db


def carga_inicial() -> None:
    """Ejecuta la carga inicial del data warehouse."""
    init_db()

    conn = psycopg2.connect(dsn=DB_URI)
    try:
        with conn.cursor() as cur:
            # TODO: implementar lógica de carga inicial
            pass
        conn.commit()
    finally:
        conn.close()


if __name__ == "__main__":
    carga_inicial()
