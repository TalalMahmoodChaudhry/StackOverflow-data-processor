import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

from constants import POSTGRES_DATABASE_ENV_VAR

SQLALCHEMY_DATABASE_URL = os.environ.get(POSTGRES_DATABASE_ENV_VAR, "sqlite:///./sql_app.db")

engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)

Base = declarative_base()
