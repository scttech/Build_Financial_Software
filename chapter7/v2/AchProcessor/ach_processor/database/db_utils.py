import os

import psycopg

POSTGRES_USER = os.getenv("POSTGRES_USER") or "someuser"
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD") or "supersecret"
POSTGRES_HOST = os.getenv("POSTGRES_HOST") or "localhost"
POSTGRES_PORT = os.getenv("POSTGRES_PORT") or "5432"

DATABASE_URL = f"dbname={POSTGRES_USER} user={POSTGRES_USER} password={POSTGRES_PASSWORD} host={POSTGRES_HOST} port={POSTGRES_PORT}"

def get_db_connection(row_factory = None):
    conn = psycopg.connect(DATABASE_URL, row_factory=row_factory)
    return conn