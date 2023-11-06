import os
from os import getenv as os_getenv

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine(os_getenv("DATABASE_URL"))
Base = declarative_base()
