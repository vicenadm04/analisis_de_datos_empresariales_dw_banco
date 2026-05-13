import os

import psycopg2
from config import DB_URI
from config import SCHEMA_STAGING

SQL_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "sql")


def _read_sql(filename: str) -> str:
    path = os.path.join(SQL_DIR, filename)
    with open(path, encoding="utf-8") as f:
        return f.read()


def carga_dim_tiempo() -> None:
    """Genera la dimensión dim_tiempo ejecutando generar_dim_tiempo.sql."""
    try:
        connection = psycopg2.connect(dsn=DB_URI)
        cursor = connection.cursor()

        cursor.execute(_read_sql("generar_dim_tiempo.sql"))

        connection.commit()
        cursor.close()
        connection.close()
        print("dim_tiempo cargada correctamente.")

    except psycopg2.Error as e:
        print(f"Error al cargar dim_tiempo: {e}")


def carga_dim_sucursal() -> None:
    """Carga la dimensión dim_sucursal ejecutando load_dim_sucursal.sql."""
    try:
        connection = psycopg2.connect(dsn=DB_URI)
        cursor = connection.cursor()

        cursor.execute(_read_sql("load_dim_sucursal.sql"))

        connection.commit()
        cursor.close()
        connection.close()
        print("dim_sucursal cargada correctamente.")

    except psycopg2.Error as e:
        print(f"Error al cargar dim_sucursal: {e}")


def carga_dim_prestatario() -> None:
    """Carga la dimensión dim_prestatario en el warehouse a partir de staging."""
    last_row = None
    try:
        connection = psycopg2.connect(dsn=DB_URI)
        cursor = connection.cursor()

        query_clientes = (
            f"SELECT DISTINCT ON (id_cliente) * FROM {SCHEMA_STAGING}.stg_clientes;"
        )
        cursor.execute(query_clientes)

        resultados_clientes = cursor.fetchall()
        for row in resultados_clientes:
            last_row = row

            gender = row[3]

            if gender not in ["M", "F", "X"]:
                gender = "X"

            fecha_inicio_vigencia = row[13]
            ingreso_mensual = None
            if row[14] is not None:
                try:
                    ingreso_mensual = float(row[14]) / 12
                except:
                    ingreso_mensual = None

            cursor.execute(
                "INSERT INTO dw_banco.dim_prestatario (codigo_prestatario, fecha_nacimiento, cantidad_hijos, ingreso_mensual, direccion, ciudad, codigo_provincia, provincia, fecha_inicio_vigencia, genero, propiedad) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (
                    row[0],
                    row[4],
                    0,
                    ingreso_mensual,
                    row[7],
                    row[8],
                    row[9],
                    row[10],
                    fecha_inicio_vigencia,
                    gender,
                    row[18],
                ),
            )

        connection.commit()
        cursor.close()
        connection.close()

    except psycopg2.Error as e:
        print(f"Error al cargar dim_prestatario: {e}")
        print(last_row)


def carga_dim_tipo_prestamo() -> None:
    """Carga la dimensión dim_tipo_prestamo ejecutando load_dim_tipo_prestamo.sql."""
    try:
        connection = psycopg2.connect(dsn=DB_URI)
        cursor = connection.cursor()

        cursor.execute(_read_sql("load_dim_tipo_prestamo.sql"))

        connection.commit()
        cursor.close()
        connection.close()
        print("dim_tipo_prestamo cargada correctamente.")

    except psycopg2.Error as e:
        print(f"Error al cargar dim_tipo_prestamo: {e}")


def carga_dim_proposito() -> None:
    """Carga la dimensión dim_proposito ejecutando load_dim_proposito.sql."""
    try:
        connection = psycopg2.connect(dsn=DB_URI)
        cursor = connection.cursor()

        cursor.execute(_read_sql("load_dim_proposito.sql"))

        connection.commit()
        cursor.close()
        connection.close()
        print("dim_proposito cargada correctamente.")

    except psycopg2.Error as e:
        print(f"Error al cargar dim_proposito: {e}")


def carga_dim_estado_prestamo() -> None:
    """Carga la dimensión dim_estado_prestamo ejecutando load_dim_estado_prestamo.sql."""
    try:
        connection = psycopg2.connect(dsn=DB_URI)
        cursor = connection.cursor()

        cursor.execute(_read_sql("load_dim_estado_prestamo.sql"))

        connection.commit()
        cursor.close()
        connection.close()
        print("dim_estado_prestamo cargada correctamente.")

    except psycopg2.Error as e:
        print(f"Error al cargar dim_estado_prestamo: {e}")


def carga_dim_descuento() -> None:
    """Carga la dimensión dim_descuento ejecutando load_dim_descuento.sql."""
    try:
        connection = psycopg2.connect(dsn=DB_URI)
        cursor = connection.cursor()

        cursor.execute(_read_sql("load_dim_descuento.sql"))

        connection.commit()
        cursor.close()
        connection.close()
        print("dim_descuento cargada correctamente.")

    except psycopg2.Error as e:
        print(f"Error al cargar dim_descuento: {e}")


if __name__ == "__main__":
    carga_dim_tiempo()
    carga_dim_sucursal()
    carga_dim_prestatario()
    carga_dim_tipo_prestamo()
    carga_dim_proposito()
    carga_dim_estado_prestamo()
    carga_dim_descuento()
