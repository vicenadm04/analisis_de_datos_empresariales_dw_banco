# 🏦 Data Warehouse Banco - Etapa de Ingesta (ETL)

Este proyecto automatiza la fase de **Extracción y Carga (EL)** de un Data Warehouse bancario. El sistema procesa archivos CSV con datos de clientes, préstamos y sucursales, realiza una limpieza técnica y los inyecta en un esquema de `staging` en PostgreSQL.

## 🚀 Características del Pipeline

* **Modularidad:** Separación de configuración (`config.py`), utilidades (`utils.py`) y lógica de ingesta.
* **Sanitización Técnica:** Limpieza física de bytes nulos (`0x00`) para asegurar la compatibilidad con el motor de base de datos (PostgreSQL).
* **Normalización de Entidades:** Mapeo inteligente de archivos basado en prefijos (ej. `loan_2019.csv` o `prestamos_v2.csv` -> tabla `stg_prestamos`).
* **Seguridad:** Gestión de credenciales mediante variables de entorno y protección con `.gitignore`.

## 🛠️ Stack Tecnológico e Instalación

Este proyecto utiliza **[uv](https://github.com/astral-sh/uv)**, el gestor de paquetes de Python más moderno y rápido, que garantiza entornos aislados y reproducibles.

### 📦 Gestión de Dependencias

Las librerías principales utilizadas y gestionadas automáticamente son:

| Librería | Función |
| --- | --- |
| **Polars** | Procesamiento de DataFrames de alto rendimiento. |
| **SQLAlchemy** | Motor de comunicación robusto y flexible con la DB. |
| **PyArrow** | Intercambio eficiente de datos en memoria. |
| **Python-dotenv** | Manejo de variables de entorno para seguridad. |
| **Psycopg2-binary** | Driver oficial para PostgreSQL. |

### ⚙️ Configuración del Entorno (Al clonar por primera vez)

1. **Clonar el repositorio:**
```bash
git clone https://github.com/vicenadm04/analisis_de_datos_empresariales_dw_banco.git
cd dw_banco

```


2. **Instalar dependencias:**
Usamos pip para gestionar las librerías necesarias (Pandas, SQLAlchemy, etc.):
```bash
pip install -r requirements.txt

```


3. **Variables de Entorno:**
Crea un archivo `.env` en la raíz del proyecto para que el sistema reconozca tu base de datos (este archivo es ignorado por Git por seguridad):
```text
DB_URI=postgresql://usuario:contraseña@localhost:5432/dw_banco
DB_NAME=dw_banco
SCHEMA_STAGING=stg_banco

```



## 📂 Estructura del Proyecto

```text
DW_banco/
├── data/
│   ├── landing/          # Archivos CSV crudos entrantes
│   └── processed/        # Historial de archivos procesados exitosamente
├── scripts/
│   ├── config.py         # Carga y validación de variables de entorno
│   ├── utils.py          # Lógica compartida de sanitización de bytes
│   └── etl_ingesta.py    # Motor principal de ingesta modular
├── .env                  # Credenciales reales (OCULTO / NO SUBIR)
├── .gitignore            # Reglas para evitar subir basura o datos sensibles
├── pyproject.toml        # Declaración formal de requerimientos
└── uv.lock               # Estado exacto del entorno (garantiza reproducibilidad)

```

## 🏃 Modo de Uso

1. Coloca tus archivos CSV en la carpeta `data/landing/`. El sistema reconoce archivos que comiencen con: `loan`, `clientes` o `sucursales`.
2. Ejecuta el pipeline:
```bash
# 1. Inicializa la base de datos y esquemas
python scripts/init_db.py

# 2. Carga de datos maestros iniciales
python scripts/carga_inicial.py

# 3. Procesa y limpia archivos de data/landing a la capa Staging
python scripts/carga_staging.py

# 4. Carga final al Data Warehouse (Dimensiones y Hechos)
python scripts/carga_warehouse.py

```



El script detectará los archivos, los limpiará de caracteres prohibidos, agregará columnas de auditoría (`stg_fecha_carga`, `stg_origen_archivo`), los subirá a PostgreSQL y finalmente moverá los archivos a `data/processed/`.

## 🛡️ Seguridad y Robustez

* **Cero Credenciales en Git:** El archivo `.gitignore` protege tu `.env`.
* **Manejo de Errores:** Si la carga en la base de datos falla, el archivo **no** se mueve a la carpeta `processed`, permitiendo la corrección y reintento sin duplicar datos.
* **Limpieza de Bytes:** Se eliminan caracteres `0x00` que suelen romper los procesos de copia en bases de datos relacionales.

---

