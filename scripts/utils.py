# scripts/utils.py

def sanitizar_bytes(ruta_archivo):
    """
    Lee un archivo y elimina los bytes nulos (0x00) 
    para que Postgres no rechace la carga.
    """
    with open(ruta_archivo, "rb") as f:
        # Lee el contenido binario y reemplaza el byte nulo por nada
        return f.read().replace(b"\x00", b"")