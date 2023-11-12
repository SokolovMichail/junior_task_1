from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database, database_exists

from app.config import Settings

Base = declarative_base()


def run_migrations(script_location: str) -> None:
    print('Running DB migrations', script_location)
    alembic_cfg = Config()
    alembic_cfg.set_main_option('script_location', script_location)
    command.upgrade(alembic_cfg, 'head')


def validate_database():
    engine = create_engine(Settings.DATABASE_URL)
    if not database_exists(engine.url):  # Checks for the first time
        create_database(engine.url)  # Create new DB
        print("New Database Created" + database_exists(engine.url))  # Verifies if database is there or not.
    else:
        print("Database Already Exists")
    run_migrations("alembic")


validate_database()
engine = create_engine(Settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

db = SessionLocal()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
