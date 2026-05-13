import csv
import io
import logging
import os
import shutil
import time

import psycopg2
from sqlalchemy import create_engine

import config
import utils

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

SCHEMA_STAGING = config.SCHEMA_STAGING


def obtener_entidad(nombre_archivo):
    """
    Identifica la entidad basándose en el inicio del nombre del archivo.
    """
    nombre_min = nombre_archivo.lower()

    if nombre_min.startswith("loan"):
        return "loan"
    elif nombre_min.startswith("clientes"):
        return "clientes"
    elif nombre_min.startswith("sucursales"):
        return "sucursales"

    return None


def _extraer_columnas_csv(buffer: io.BytesIO) -> list[str]:
    """Lee solo la primera línea del buffer para obtener los nombres de columna."""
    primera_linea = buffer.readline().decode("utf-8", errors="replace")
    reader = csv.reader(io.StringIO(primera_linea))
    return [col.strip() for col in next(reader)]


def _crear_tabla_staging(
    cursor: psycopg2.extensions.cursor, schema: str, tabla: str, columnas_csv: list[str]
) -> None:
    """
    Crea (o recrea) la tabla de staging con las columnas del CSV como TEXT
    más las columnas de auditoría.
    """
    tabla_full = f"{schema}.{tabla}"
    cursor.execute(f"DROP TABLE IF EXISTS {tabla_full}")

    cols_sql = ", ".join(f'"{col}" TEXT' for col in columnas_csv)
    ddl = f"""
        CREATE TABLE {tabla_full} (
            {cols_sql},
            stg_fecha_carga TIMESTAMP DEFAULT NOW(),
            stg_origen_archivo TEXT
        )
    """
    cursor.execute(ddl)
    logger.info(
        "  Tabla %s creada (%d columnas del CSV + 2 de auditoría).",
        tabla_full,
        len(columnas_csv),
    )


def _copiar_csv(
    cursor: psycopg2.extensions.cursor,
    schema: str,
    tabla: str,
    columnas_csv: list[str],
    buffer: io.BytesIO,
    nombre_archivo: str,
) -> tuple[int, float]:
    """
    Ejecuta COPY FROM STDIN para cargar el contenido del CSV en la tabla.
    El buffer ya debe estar posicionado después del header.
    """
    tabla_full = f"{schema}.{tabla}"
    cols_list = ", ".join(f'"{col}"' for col in columnas_csv)

    copy_sql = f"""
        COPY {tabla_full} ({cols_list})
        FROM STDIN
        WITH (FORMAT csv, HEADER false, DELIMITER ',', NULL '')
    """

    t_inicio = time.perf_counter()
    cursor.copy_expert(copy_sql, buffer)
    filas = cursor.rowcount
    duracion = time.perf_counter() - t_inicio

    cursor.execute(
        f"UPDATE {tabla_full} SET stg_origen_archivo = %s WHERE stg_origen_archivo IS NULL",
        (nombre_archivo,),
    )

    return filas, duracion


def ejecutar_ingesta():
    folder_landing = "data/landing"
    folder_processed = "data/processed"

    os.makedirs(folder_processed, exist_ok=True)

    archivos = [f for f in os.listdir(folder_landing) if f.endswith(".csv")]

    if not archivos:
        logger.info("No hay archivos nuevos para procesar en %s.", folder_landing)
        return

    logger.info("Encontrados %d archivo(s) CSV en %s.", len(archivos), folder_landing)

    engine = create_engine(config.DB_URI)
    conn = engine.raw_connection()

    try:
        for nombre_archivo in archivos:
            entidad = obtener_entidad(nombre_archivo)

            if entidad is None:
                logger.warning(
                    "Ignorando '%s': no coincide con loan, clientes o sucursales.",
                    nombre_archivo,
                )
                continue

            ruta_origen = os.path.join(folder_landing, nombre_archivo)
            tabla_nom = f"stg_{entidad}"

            logger.info(
                "Procesando '%s' -> %s.%s ...",
                nombre_archivo,
                SCHEMA_STAGING,
                tabla_nom,
            )

            try:
                datos_limpios = utils.sanitizar_bytes(ruta_origen)
                tamano_mb = len(datos_limpios) / (1024 * 1024)
                logger.info("  Archivo sanitizado (%.2f MB en memoria).", tamano_mb)

                buffer = io.BytesIO(datos_limpios)

                columnas_csv = _extraer_columnas_csv(buffer)
                logger.info(
                    "  Columnas detectadas: %d -> %s",
                    len(columnas_csv),
                    columnas_csv[:5],
                )

                cursor = conn.cursor()
                _crear_tabla_staging(cursor, SCHEMA_STAGING, tabla_nom, columnas_csv)

                logger.info("  Ejecutando COPY FROM STDIN ...")
                filas, duracion = _copiar_csv(
                    cursor,
                    SCHEMA_STAGING,
                    tabla_nom,
                    columnas_csv,
                    buffer,
                    nombre_archivo,
                )
                conn.commit()

                vel = filas / duracion if duracion > 0 else 0
                logger.info(
                    "  COPY finalizado: %d filas en %.2fs (%.0f filas/s).",
                    filas,
                    duracion,
                    vel,
                )

                shutil.move(ruta_origen, os.path.join(folder_processed, nombre_archivo))
                logger.info("  Archivo movido a %s.", folder_processed)

            except Exception:
                conn.rollback()
                logger.exception("Error al procesar '%s'.", nombre_archivo)

    finally:
        conn.close()
        engine.dispose()

    logger.info("Ingesta completa.")


if __name__ == "__main__":
    ejecutar_ingesta()
