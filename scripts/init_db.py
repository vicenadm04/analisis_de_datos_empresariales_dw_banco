import os

import psycopg2
from psycopg2 import sql

from config import DB_NAME, DB_URI, DB_URI_SERVER, SCHEMA_STAGING

SQL_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "sql")


def _read_sql(filename: str) -> str:
    path = os.path.join(SQL_DIR, filename)
    with open(path, encoding="utf-8") as f:
        return f.read()


def _ensure_database() -> None:
    """Crea la base de datos si no existe, con configuración UTF-8."""
    conn = psycopg2.connect(dsn=DB_URI_SERVER)
    try:
        conn.autocommit = True
        with conn.cursor() as cur:
            cur.execute(
                "SELECT 1 FROM pg_database WHERE datname = %s;", (DB_NAME,)
            )
            if cur.fetchone() is not None:
                print(f"Base de datos '{DB_NAME}' ya existe.")
                return

            print(f"Base de datos '{DB_NAME}' no encontrada. Creando…")
            cur.execute(
                sql.SQL(
                    "CREATE DATABASE {db} "
                    "ENCODING 'UTF8' "
                    "LC_COLLATE 'C' "
                    "LC_CTYPE 'C' "
                    "TEMPLATE template0;"
                ).format(db=sql.Identifier(DB_NAME))
            )
            print(f"Base de datos '{DB_NAME}' creada correctamente.")
    finally:
        conn.close()


def _ensure_staging_schema(cursor) -> None:
    """Crea el esquema de staging si no existe (solo el schema, sin tablas)."""
    cursor.execute(
        sql.SQL("CREATE SCHEMA IF NOT EXISTS {};").format(
            sql.Identifier(SCHEMA_STAGING)
        )
    )
    print(f"Esquema '{SCHEMA_STAGING}' listo.")


def _schema_exists(cursor) -> bool:
    cursor.execute(
        "SELECT 1 FROM information_schema.schemata WHERE schema_name = 'dw_banco';"
    )
    return cursor.fetchone() is not None


def _tables_exist(cursor) -> bool:
    cursor.execute(
        """
        SELECT 1 FROM information_schema.tables
        WHERE table_schema = 'dw_banco'
        LIMIT 1;
        """
    )
    return cursor.fetchone() is not None


def init_db() -> None:
    """Inicializa la base de datos y el esquema dw_banco de forma idempotente.

    1. Crea la base de datos si no existe (UTF-8, locale C).
    2. Si el esquema no existe, lo crea junto con todas las tablas (schema.sql).
    3. Si el esquema ya existe y tiene tablas, las vacía por completo.
    """
    _ensure_database()

    conn = psycopg2.connect(dsn=DB_URI)
    try:
        conn.autocommit = True
        with conn.cursor() as cur:
            _ensure_staging_schema(cur)

            if not _schema_exists(cur):
                print("Esquema dw_banco no encontrado. Creando esquema y tablas…")
                cur.execute(_read_sql("schema.sql"))
                print("Esquema y tablas creados correctamente.")
            elif _tables_exist(cur):
                print("Esquema dw_banco encontrado. Vaciando tablas…")
                cur.execute(_read_sql("truncate_tables.sql"))
                print("Tablas vaciadas correctamente.")
            else:
                print("Esquema dw_banco existe pero sin tablas. Creando tablas…")
                cur.execute(_read_sql("schema.sql"))
                print("Tablas creadas correctamente.")

            print("Registrando funciones y utilidades…")
            cur.execute(_read_sql("functions_and_utils.sql"))
            print("Funciones y utilidades registradas correctamente.")
    finally:
        conn.close()


if __name__ == "__main__":
    init_db()
