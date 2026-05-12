import os
import sys
import psycopg2

# Cargar el URI de la base de datos desde config.py
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)
from config import DB_URI

try:
    # Conectar a la base de datos usando el URI
    connection = psycopg2.connect(dsn=DB_URI)
    
    # Crear un cursor
    cursor = connection.cursor()
    
    # Consulta de ejemplo: seleccionar todos los registros de una tabla (reemplaza 'tu_tabla' con el nombre real)
    query = "SELECT * FROM tu_tabla LIMIT 10;"  # Ajusta la consulta según necesites
    cursor.execute(query)
    
    # Obtener y mostrar resultados
    results = cursor.fetchall()
    for row in results:
        # Verificar si el primer atributo (columna 0) es nulo y reemplazarlo con un valor por defecto
        if row[0] is None:
            row = ("valor_por_defecto",) + row[1:]  # Reemplaza "valor_por_defecto" con el valor deseado
        print(row)
    
    # Insertar los resultados procesados en otra tabla (ajusta las columnas y valores según la estructura de 'otra_tabla')
    # Ejemplo: si 'otra_tabla' tiene 2 columnas y 'tu_tabla' tiene más, inserta solo las primeras 2
    for row in results:
        cursor.execute("INSERT INTO otra_tabla (col1, col2) VALUES (%s, %s)", (row[0], row[1]))  # Ajusta según las columnas reales
    
    # Confirmar los cambios
    connection.commit()
    
    # Cerrar cursor y conexión
    cursor.close()
    connection.close()
    
except psycopg2.Error as e:
    print(f"Error al conectar o consultar la base de datos: {e}")