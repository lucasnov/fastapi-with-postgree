import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"postgresql+psycopg://{os.getenv('POSTGRES_USER', 'projeto')}:"
    f"{os.getenv('POSTGRES_PASSWORD', 'projeto')}@db:5432/"
    f"{os.getenv('POSTGRES_DB', 'projeto')}"
)

engine = create_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()
