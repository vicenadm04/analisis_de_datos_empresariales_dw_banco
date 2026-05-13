# scripts/config.py
import os
from urllib.parse import urlparse, urlunparse

from dotenv import load_dotenv

load_dotenv()

DB_URI = os.getenv("DB_URI")
DB_NAME = os.getenv("DB_NAME")
SCHEMA_STAGING = os.getenv("SCHEMA_STAGING")

if not DB_URI:
    raise ValueError("No se encontró DB_URI en el archivo .env")
if not DB_NAME:
    raise ValueError("No se encontró DB_NAME en el archivo .env")
if not SCHEMA_STAGING:
    raise ValueError("No se encontró SCHEMA_STAGING en el archivo .env")

_parsed = urlparse(DB_URI)
DB_URI_SERVER = urlunparse(_parsed._replace(path="/postgres"))