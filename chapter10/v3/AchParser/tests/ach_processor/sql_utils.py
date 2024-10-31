import os
from uuid import UUID

import psycopg
from psycopg import Connection
from psycopg.sql import SQL, Identifier

from chapter10.v3.AchParser.ach_processor.database.ach_file_header_sql import (
    AchFileHeaderSql,
)
from chapter10.v3.AchParser.ach_processor.database.ach_file_sql import AchFileSql
from chapter10.v3.AchParser.ach_processor.database.ach_records_sql_type_1 import (
    AchRecordsSqlType1,
)
from chapter10.v3.AchParser.ach_processor.database.ach_records_sql_type_5 import (
    AchRecordsSqlType5,
)
from chapter10.v3.AchParser.ach_processor.database.ach_records_sql_type_6 import (
    AchRecordsSqlType6,
)
from chapter10.v3.AchParser.ach_processor.database.ach_records_sql_type_7 import (
    AchRecordsSqlType7,
)
from chapter10.v3.AchParser.ach_processor.database.ach_records_sql_type_8 import (
    AchRecordsSqlType8,
)
from chapter10.v3.AchParser.ach_processor.database.ach_records_sql_type_9 import (
    AchRecordsSqlType9,
)
from chapter10.v3.AchParser.ach_processor.schemas.database.ach_file_header_schema import (
    AchFileHeaderSchema,
)
from chapter10.v3.AchParser.ach_processor.schemas.database.ach_file_schema import (
    AchFileSchema,
)
from chapter10.v3.AchParser.ach_processor.schemas.database.ach_record.ach_record_type_1_schema import (
    AchRecordType1Schema,
)
from chapter10.v3.AchParser.ach_processor.schemas.database.ach_record.ach_record_type_5_schema import (
    AchRecordType5Schema,
)
from chapter10.v3.AchParser.ach_processor.schemas.database.ach_record.ach_record_type_6_schema import (
    AchRecordType6Schema,
)
from chapter10.v3.AchParser.ach_processor.schemas.database.ach_record.ach_record_type_7_schema import (
    AchRecordType7Schema,
)
from chapter10.v3.AchParser.ach_processor.schemas.database.ach_record.ach_record_type_8_schema import (
    AchRecordType8Schema,
)
from chapter10.v3.AchParser.ach_processor.schemas.database.ach_record.ach_record_type_9_schema import (
    AchRecordType9Schema,
)

POSTGRES_USER = os.getenv("POSTGRES_USER") or "postgres"
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD") or "postgres"
POSTGRES_HOST = os.getenv("POSTGRES_HOST") or "localhost"
POSTGRES_PORT = os.getenv("POSTGRES_PORT") or "5432"

DATABASE_URL = (
    f"dbname={POSTGRES_USER} user={POSTGRES_USER} "
    f"password={POSTGRES_PASSWORD} host={POSTGRES_HOST} port={POSTGRES_PORT}"
)


class SqlUtils:
    @staticmethod
    def get_db(row_factory=None) -> Connection:
        """Get a connection to the database."""
        try:
            conn = psycopg.connect(DATABASE_URL, row_factory=row_factory)
        except Exception as e:
            print(e)
            raise e
        return conn

    @staticmethod
    def get_row_count_of_1(table_name: str = "") -> bool:
        """Return True if the table has exactly one row, False otherwise."""
        with SqlUtils.get_db() as conn:
            query = SQL("SELECT COUNT(*) FROM {table_name}").format(
                table_name=Identifier(table_name)
            )
            record_count = conn.execute(query).fetchone()[0]
        return record_count == 1

    @staticmethod
    def truncate(table_name: str = "") -> None:
        """Truncate the table."""
        with SqlUtils.get_db() as conn:
            query = SQL("TRUNCATE {table_name}").format(
                table_name=Identifier(table_name)
            )
            conn.execute(query)

    @staticmethod
    def get_exceptions() -> list:
        """Return a list of exceptions as a flattened list."""
        with SqlUtils.get_db() as conn:
            exceptions = conn.execute(
                """
                SELECT exception_code
                FROM ach_exceptions AS afe
                """
            ).fetchall()
        flattened_list = [item[0] for item in exceptions]
        return flattened_list

    @staticmethod
    def create_ach_file_record(file_name: str, file_hash: str) -> str:
        """
        Create a dummy record in the ach_files table to use as a foreign key.
        :return:
        """
        ach_file_id = AchFileSql().insert_record(
            AchFileSchema(file_name=file_name, file_hash=file_hash)
        )

        return ach_file_id.hex

    @staticmethod
    def setup_file_header_test(unparsed_record: str) -> UUID:
        """
        Create a dummy record in the ach_records table to use as a foreign key.
        :return:
        """
        ach_file_id = SqlUtils.create_ach_file_record("sample.ach", "123456789")
        ach_record_id = AchRecordsSqlType1().insert_record(
            AchRecordType1Schema(
                ach_files_id=ach_file_id,
                file_name="pytest.ach",
                unparsed_record=unparsed_record,
                sequence_number=1,
            )
        )

        return ach_record_id

    @staticmethod
    def create_ach_file_header() -> UUID:
        """
        Create a dummy record in the ach_file_headers table to use as a foreign key.
        :return:
        """
        ach_file_id = SqlUtils.create_ach_file_record("sample.ach", "123456789")
        ach_record_id = AchRecordsSqlType1().insert_record(
            AchRecordType1Schema(
                ach_files_id=ach_file_id,
                file_name="pytest.ach",
                unparsed_record="101 267084131 6910001340402200830A094101DEST NAME              ORIGIN NAME            XXXXXXXX",
                sequence_number=1,
            )
        )
        ach_file_header_id = AchFileHeaderSql().insert_record(
            AchFileHeaderSchema(
                ach_records_id=ach_record_id,
                record_type_code="1",
                priority_code="01",
                immediate_destination="267084131",
                immediate_origin="691000134",
                file_creation_date="040220",
                file_creation_time="0830",
                file_id_modifier="A",
                record_size="094",
                blocking_factor="10",
                format_code="1",
                immediate_destination_name="DEST NAME",
                immediate_origin_name="ORIGIN NAME",
                reference_code="XXXXXXXX",
                file_record_modifier="P",
                ach_operator_data="PD",
            )
        )

        return ach_file_header_id

    @staticmethod
    def setup_batch_header_test(sample_batch_header_record: str):
        """
        Creates the following dummy records:
        ach_file
        ach_record (file header)
        ach_file_header
        ach_record (batch record)
        :return:
        """
        # Create the dummy ach_file record to represent the upload
        ach_file_id = SqlUtils.create_ach_file_record("sample.ach", "123456789")
        # Create a dummy file header record
        ach_records_type_1_id = AchRecordsSqlType1().insert_record(
            AchRecordType1Schema(
                ach_files_id=ach_file_id,
                unparsed_record="101 267084131 6910001340402200830A094101DEST NAME              ORIGIN NAME            XXXXXXXX",
                sequence_number=1,
            )
        )
        # Create a dummy batch header record
        ach_records_type_5_id = AchRecordsSqlType5().insert_record(
            AchRecordType5Schema(
                ach_records_type_1_id=ach_records_type_1_id,
                unparsed_record=sample_batch_header_record,
                sequence_number=2,
            )
        )

        return ach_records_type_1_id, ach_records_type_5_id

    @staticmethod
    def setup_batch_control_test(sample_batch_control_record):
        """
        Creates the following dummy records:
        ach_file
        ach_record (file header)
        ach_record (batch record)
        ach_record (batch control)
        :return:
        """
        # Create the dummy ach_file record to represent the upload
        ach_file_id = SqlUtils.create_ach_file_record("sample.ach", "123456789")
        # Create a dummy file header record
        ach_records_type_1_id = AchRecordsSqlType1().insert_record(
            AchRecordType1Schema(
                ach_files_id=ach_file_id,
                unparsed_record="101 267084131 6910001340402200830A094101DEST NAME              ORIGIN NAME            XXXXXXXX",
                sequence_number=1,
            )
        )
        # Create a dummy batch header record
        ach_records_type_5_id = AchRecordsSqlType5().insert_record(
            AchRecordType5Schema(
                ach_records_type_1_id=ach_records_type_1_id,
                unparsed_record="5200Company name    DiscretionaryData   Company IDARCComp desc 0216232302160471061000010000001",
                sequence_number=2,
            )
        )
        # Create a dummy batch control record
        ach_records_type_8_id = AchRecordsSqlType8().insert_record(
            AchRecordType8Schema(
                ach_records_type_5_id=ach_records_type_5_id,
                unparsed_record=sample_batch_control_record,
                sequence_number=3,
            )
        )

        return ach_records_type_5_id, ach_records_type_8_id

    @staticmethod
    def setup_file_control_test(sample_file_control_record):
        """
        Creates the following dummy records:
        ach_file
        ach_record (file header)
        ach_record (file control record)
        :return:
        """
        # Create the dummy ach_file record to represent the upload
        ach_file_id = SqlUtils.create_ach_file_record("sample.ach", "123456789")
        # Create a dummy file header record
        ach_records_type_1_id = AchRecordsSqlType1().insert_record(
            AchRecordType1Schema(
                ach_files_id=ach_file_id,
                unparsed_record="101 267084131 6910001340402200830A094101DEST NAME              ORIGIN NAME            XXXXXXXX",
                sequence_number=1,
            )
        )
        # Create a dummy file control record
        ach_records_type_9_id = AchRecordsSqlType9().insert_record(
            AchRecordType9Schema(
                ach_records_type_1_id=ach_records_type_1_id,
                unparsed_record=sample_file_control_record,
                sequence_number=2,
            )
        )

        return ach_records_type_1_id, ach_records_type_9_id

    @staticmethod
    def setup_entry_ppd_details_test(sample_ach_entry_ppd_details_record):
        """
        Creates the following dummy records:
        ach_file
        ach_record (file header)
        ach_record (batch record)
        ach_record (entry detail record)
        :return:
        """
        # Create the dummy ach_file record to represent the upload
        ach_file_id = SqlUtils.create_ach_file_record("sample.ach", "123456789")
        # Create a dummy file header record
        ach_records_type_1_id = AchRecordsSqlType1().insert_record(
            AchRecordType1Schema(
                ach_files_id=ach_file_id,
                unparsed_record="101 267084131 6910001340402200830A094101DEST NAME              ORIGIN NAME            XXXXXXXX",
                sequence_number=1,
            )
        )
        # Create a dummy batch header record
        ach_records_type_5_id = AchRecordsSqlType5().insert_record(
            AchRecordType5Schema(
                ach_records_type_1_id=ach_records_type_1_id,
                unparsed_record="5200Company name    DiscretionaryData   Company IDARCComp desc 0216232302160471061000010000001",
                sequence_number=2,
            )
        )
        # Create a entry details record
        ach_records_type_6_id = AchRecordsSqlType6().insert_record(
            AchRecordType6Schema(
                ach_records_type_5_id=ach_records_type_5_id,
                unparsed_record=sample_ach_entry_ppd_details_record,
                sequence_number=3,
            )
        )

        return ach_records_type_5_id, ach_records_type_6_id

    @staticmethod
    def setup_addenda_ppd_test(sample_ach_addenda_ppd_record):
        # Create the dummy ach_file record to represent the upload
        ach_file_id = SqlUtils.create_ach_file_record("sample.ach", "123456789")
        # Create a dummy file header record
        ach_records_type_1_id = AchRecordsSqlType1().insert_record(
            AchRecordType1Schema(
                ach_files_id=ach_file_id,
                unparsed_record="101 267084131 6910001340402200830A094101DEST NAME              ORIGIN NAME            XXXXXXXX",
                sequence_number=1,
            )
        )
        # Create a dummy batch header record
        ach_records_type_5_id = AchRecordsSqlType5().insert_record(
            AchRecordType5Schema(
                ach_records_type_1_id=ach_records_type_1_id,
                unparsed_record="5200Company name    DiscretionaryData   Company IDARCComp desc 0216232302160471061000010000001",
                sequence_number=2,
            )
        )
        # Create a dummy entry details record
        ach_records_type_6_id = AchRecordsSqlType6().insert_record(
            AchRecordType6Schema(
                ach_records_type_5_id=ach_records_type_5_id,
                unparsed_record="6220670841316910001340402200830A094101DEST NAME              ORIGIN NAME            XXXXXXXX",
                sequence_number=3,
            )
        )
        # Create a dummy addenda ppd record
        ach_records_type_7_id = AchRecordsSqlType7().insert_record(
            AchRecordType7Schema(
                ach_records_type_6_id=ach_records_type_6_id,
                unparsed_record=sample_ach_addenda_ppd_record,
                sequence_number=4,
            )
        )

        return ach_records_type_6_id, ach_records_type_7_id

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
                FOR r IN SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' AND table_type = 'BASE TABLE' AND table_name NOT IN ('ach_exception_codes', 'ach_recovery_options', 'bank_routing_numbers')
                LOOP
                    EXECUTE 'ALTER TABLE ' || quote_ident(r.table_name) || ' DISABLE TRIGGER ALL';
                END LOOP;

                -- Truncate all tables
                EXECUTE (
                    SELECT 'TRUNCATE TABLE ' || string_agg(quote_ident(table_name), ', ') || ' CASCADE'
                    FROM information_schema.tables
                    WHERE table_schema = 'public'
                    AND table_type = 'BASE TABLE'
                    AND table_name NOT IN ('ach_exception_codes', 'ach_recovery_options', 'bank_routing_numbers')                    
                );

                -- Re-enable triggers
                FOR r IN SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' AND table_type = 'BASE TABLE' AND table_name NOT IN ('ach_exception_codes', 'ach_recovery_options', 'bank_routing_numbers')
                LOOP
                    EXECUTE 'ALTER TABLE ' || quote_ident(r.table_name) || ' ENABLE TRIGGER ALL';
                END LOOP;
            END $$;
            """
            conn.execute(sql)
