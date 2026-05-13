import polars as pl
from datetime import datetime
import io
import os
import shutil
import config  # Asegúrate de tener DB_URI aquí
import utils  # Asegúrate de tener la función sanitizar_bytes aquí


SCHEMA_STAGING = config.SCHEMA_STAGING


def obtener_entidad(nombre_archivo):
    """
    Identifica la entidad basándose en el inicio del nombre del archivo.
    """
    nombre_min = nombre_archivo.lower()

    # Definimos estrictamente tus 3 entidades
    if nombre_min.startswith("loan"):
        return "loan"
    elif nombre_min.startswith("clientes"):
        return "clientes"
    elif nombre_min.startswith("sucursales"):
        return "sucursales"

    return None  # Si no es ninguno de los 3


def ejecutar_ingesta():
    folder_landing = "data/landing"
    folder_processed = "data/processed"

    os.makedirs(folder_processed, exist_ok=True)

    # Listamos archivos CSV en landing
    archivos = [f for f in os.listdir(folder_landing) if f.endswith(".csv")]

    if not archivos:
        print("📭 No hay archivos nuevos para procesar.")
        return

    for nombre_archivo in archivos:
        entidad = obtener_entidad(nombre_archivo)

        if entidad is None:
            print(
                f"⚠️ Ignorando {nombre_archivo}: No empieza con prestamos, clientes o sucursales."
            )
            continue

        ruta_origen = os.path.join(folder_landing, nombre_archivo)
        tabla_nom = f"stg_{entidad}"

        print(f"⌛ Procesando {entidad} (Archivo: {nombre_archivo})...")

        try:
            # 1. Limpieza de bytes prohibidos
            datos_limpios = utils.sanitizar_bytes(ruta_origen)

            # 2. Lectura con Polars
            df = pl.read_csv(io.BytesIO(datos_limpios), encoding="utf8-lossy")

            # 3. Metadatos de auditoría
            df = df.with_columns(
                [
                    pl.lit(datetime.now()).alias("stg_fecha_carga"),
                    pl.lit(nombre_archivo).alias("stg_origen_archivo"),
                ]
            )

            # 4. Carga a Postgres
            df.write_database(
                table_name=f"{SCHEMA_STAGING}.{tabla_nom}",
                connection=config.DB_URI,
                if_table_exists="append",
                engine="sqlalchemy",
            )

            # 5. Movimiento a Processed
            shutil.move(ruta_origen, os.path.join(folder_processed, nombre_archivo))
            print(f"✅ Cargado en {SCHEMA_STAGING}.{tabla_nom} y movido a processed.")

        except Exception as e:
            print(f"❌ Error al procesar {nombre_archivo}: {e}")


if __name__ == "__main__":
    ejecutar_ingesta()
