import psycopg

POSTGRES_USER = "someuser"
POSTGRES_PASSWORD = "supersecret"

DATABASE_URL = f"dbname={POSTGRES_USER} user={POSTGRES_USER} password={POSTGRES_PASSWORD} host=localhost port=5432"

class SqlUtils:
    @staticmethod
    def get_db(row_factory = None):
        """Get a connection to the database."""
        conn = psycopg.connect(DATABASE_URL, row_factory=row_factory)
        return conn

    @staticmethod
    def get_row_count_of_1(table_name: str = '') -> bool:
        """Return True if the table has exactly one row, False otherwise."""
        with SqlUtils.get_db() as conn:
            sql = f"SELECT COUNT(*) FROM {table_name}"
            record_count = conn.execute(sql).fetchone()[0]
        return record_count == 1

    @staticmethod
    def truncate(table_name: str = '') -> None:
        """Truncate the table."""
        with SqlUtils.get_db() as conn:
            conn.execute(f"TRUNCATE {table_name}")
        return

    @staticmethod
    def get_exceptions() -> list:
        """Return a list of exceptions as a flattened list."""
        with SqlUtils.get_db() as conn:
            exceptions = conn.execute(f"SELECT exception_description FROM ach_exceptions").fetchall()
        flattened_list = [item[0] for item in exceptions]
        return flattened_list

    @staticmethod
    def truncate_all() -> None:
        """Truncate all tables."""
        with SqlUtils.get_db() as conn:
            sql = """
            DO $$
            DECLARE
                r RECORD;
            BEGIN
                -- Disable triggers and collect table names
                FOR r IN SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'
                LOOP
                    EXECUTE 'ALTER TABLE ' || quote_ident(r.table_name) || ' DISABLE TRIGGER ALL';
                END LOOP;

                -- Truncate all tables
                EXECUTE (
                    SELECT 'TRUNCATE TABLE ' || string_agg(quote_ident(table_name), ', ') || ' CASCADE'
                    FROM information_schema.tables
                    WHERE table_schema = 'public'
                );

                -- Re-enable triggers
                FOR r IN SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'
                LOOP
                    EXECUTE 'ALTER TABLE ' || quote_ident(r.table_name) || ' ENABLE TRIGGER ALL';
                END LOOP;
            END $$;
            """
            conn.execute(sql)
        return
