import psycopg2
from config import DB_URI


def carga_dim_prestatario() -> None:
    """Carga la dimensión dim_prestatario en el warehouse a partir de staging."""
    try:
        connection = psycopg2.connect(dsn=DB_URI)
        cursor = connection.cursor()

        query_clientes = "SELECT DISTINCT ON (id_cliente) * FROM staging.stg_clientes;"
        cursor.execute(query_clientes)

        resultados_clientes = cursor.fetchall()
        for row in resultados_clientes:
            if row[3] is None:
                row = ("X",) + row[1:]
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

        connection.commit()
        cursor.close()
        connection.close()

    except psycopg2.Error as e:
        print(f"Error al cargar dim_prestatario: {e}")


if __name__ == "__main__":
    carga_dim_prestatario()
