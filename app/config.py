from os import getenv as os_getenv


class Settings:
    PROJECT_NAME: str = "Job Board"
    PROJECT_VERSION: str = "1.0.0"

    POSTGRES_USER: str = os_getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os_getenv("POSTGRES_PASSWORD")
    POSTGRES_SERVER: str = os_getenv("POSTGRES_SERVER", "localhost")
    POSTGRES_PORT: str = os_getenv("POSTGRES_PORT", 5432)  # default postgres port is 5432
    POSTGRES_DB: str = os_getenv("POSTGRES_DB", "tdd")
    DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
