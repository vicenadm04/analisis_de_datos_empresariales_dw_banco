import psycopg2
from config import DB_URI
from init_db import init_db
from config import SCHEMA_STAGING


def carga_inicial() -> None:
    """Ejecuta la carga inicial del data warehouse."""
    init_db()

    try:
        # Conectar a la base de datos usando el URI
        connection = psycopg2.connect(dsn=DB_URI)

        # Crear un cursor
        cursor = connection.cursor()

        # Consulta de ejemplo: seleccionar todos los registros de una tabla (reemplaza 'tu_tabla' con el nombre real)
        query_clientes = "SELECT DISTINCT ON (id_cliente) * FROM staging.stg_clientes;"  # Ajusta la consulta según necesites
        cursor.execute(query_clientes)

        # Obtener, transformar y cargar a la dw
        resultados_clientes = cursor.fetchall()
        for row in resultados_clientes:
            if row[3] is None:
                row = ("X",) + row[
                    1:
                ]  # Reemplaza "valor_por_defecto" con el valor deseado
            cursor.execute(
                "INSERT INTO dw_banco.dim_prestatario (codigo_prestatario, fecha_nacimiento, cantidad_hijos, ingreso_mensual, direccion, ciudad, codigo_provincia, provincia, fecha_inicio_vigencia, genero, propiedad) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (
                    row[0],
                    row[4],
                    0,
                    row[15] / 12,
                    row[7],
                    row[8],
                    row[9],
                    row[10],
                    row[14],
                    row[3],
                    row[18],
                ),
            )

        # Confirmar los cambios
        connection.commit()

        # Cerrar cursor y conexión
        cursor.close()
        connection.close()

    except psycopg2.Error as e:
        print(f"Error al conectar o consultar la base de datos: {e}")


if __name__ == "__main__":
    carga_inicial()
