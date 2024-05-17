import psycopg
from fastapi import FastAPI

DATABASE_URL = "dbname=postgres user=postgres password=secret host=postgres port=5432"

app = FastAPI()

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
