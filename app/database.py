from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os
from sqlalchemy.orm import Session

load_dotenv()

DB_SERVER = os.getenv("DB_SERVER")
DB_DATABASE = os.getenv("DB_DATABASE")
DB_DRIVER = os.getenv("DB_DRIVER")
DB_TRUST = os.getenv("DB_TRUST")

connection_string = (
    f"mssql+pyodbc://@{DB_SERVER}/{DB_DATABASE}"
    f"?driver={DB_DRIVER.replace(' ', '+')}"
    f"&TrustServerCertificate={DB_TRUST}"
    f"&trusted_connection=yes"
)

engine = create_engine(connection_string)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        