# scripts/config.py
import os
from dotenv import load_dotenv

# Carga las variables del archivo .env
load_dotenv()

# Lee la variable o tira un error si no la encuentra
DB_URI = os.getenv("DB_URI")

if not DB_URI:
    raise ValueError("❌ No se encontró la DB_URI en el archivo .env")