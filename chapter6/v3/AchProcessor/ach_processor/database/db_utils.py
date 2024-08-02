import psycopg

POSTGRES_USER = "someuser"
POSTGRES_PASSWORD = "supersecret"

DATABASE_URL = f"dbname={POSTGRES_USER} user={POSTGRES_USER} password={POSTGRES_PASSWORD} host=localhost port=5432"

def get_db_connection(row_factory = None):
    conn = psycopg.connect(DATABASE_URL, row_factory=row_factory)
    return conn