from fastapi import FastAPI
from sqlalchemy import text
from app.database import Base, engine
from app import models
from app.routers import auth
from app.routers import users
from app.routers import patients
from app.routers import appointments

Base.metadata.create_all(bind=engine)

app = FastAPI(title="ClinicConnect API")

app.include_router(auth.router)

app.include_router(users.router)

app.include_router(patients.router)

app.include_router(appointments.router)


@app.get("/")
def home():
    return {
        "Project": "ClinicConnect",
        "Status": "Running"
    }

@app.get("/db-test")
def database_test():
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))

    return {
        "Database": "Connected Successfully"
    }
