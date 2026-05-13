from init_db import init_db


def carga_inicial() -> None:
    """Ejecuta la carga inicial del data warehouse."""
    init_db()


if __name__ == "__main__":
    carga_inicial()
