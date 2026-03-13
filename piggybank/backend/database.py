import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# The path is set by run.sh via environment variable to /data/piggybank.db. 
# Fallback to local db if running outside HA Add-on for testing.
SQLALCHEMY_DATABASE_URL = os.environ.get("DB_PATH", "sqlite:///./piggybank-dev.db")

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
