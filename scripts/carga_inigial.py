from init_db import init_db
from carga_warehouse import carga_dim_prestatario


def carga_inicial() -> None:
    """Ejecuta la carga inicial del data warehouse."""
    init_db()
    carga_dim_prestatario()


if __name__ == "__main__":
    carga_inicial()
