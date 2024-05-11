from typing import Union
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import psycopg

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")

DATABASE_URL = f"dbname={POSTGRES_USER} user={POSTGRES_USER} password={POSTGRES_PASSWORD} host=postgres port=5432"

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"],
)

def get_db():
    conn = psycopg.connect(DATABASE_URL)
    return conn


@app.get("/")
def read_root():
    return {"message": "Hello World!"}


@app.get("/health/status")
def health_status():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT id, status FROM health_check;")

    health_checks = [{"id": id, "status": status} for (id, status) in cursor.fetchall()]

    cursor.close()
    conn.close()

    return health_checks
