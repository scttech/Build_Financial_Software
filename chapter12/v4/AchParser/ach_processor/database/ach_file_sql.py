from typing import Optional
from uuid import UUID

from psycopg.rows import dict_row, class_row

from chapter12.v4.AchParser.ach_processor.database.db_utils import get_db_connection
from chapter12.v4.AchParser.ach_processor.schemas.api.ach_batch_entries_response import (
    AchBatchEntriesResponse,
)
from chapter12.v4.AchParser.ach_processor.schemas.api.ach_batches_response import (
    AchBatchesResponse,
)
from chapter12.v4.AchParser.ach_processor.schemas.api.ach_files_response import (
    AchFilesResponse,
)
from chapter12.v4.AchParser.ach_processor.schemas.database.ach_file_schema import (
    AchFileSchema,
)


class AchFileSql:
    @staticmethod
    def insert_record(ach_file: AchFileSchema) -> UUID:
        with get_db_connection() as conn:
            result = conn.execute(
                """
                INSERT INTO ach_files(ach_files_id, file_name, file_hash, created_at)
                               VALUES (DEFAULT, %(file_name)s, %(file_hash)s, DEFAULT)
                               RETURNING ach_files_id
                                """,
                ach_file.model_dump(),
            )

        return result.fetchone()[0]

    @staticmethod
    def get_records(
        limit: Optional[int] = None, offset: Optional[int] = None
    ) -> list[AchFileSchema]:
        with get_db_connection(row_factory=class_row(AchFileSchema)) as conn:
            result = conn.execute(
                """
                SELECT * FROM ach_files
                LIMIT %s 
                OFFSET %s
                """,
                [limit, offset],
            )

            return result.fetchall()

    @staticmethod
    def get_files_response(
        limit: Optional[int] = 100, offset: Optional[int] = 0
    ) -> list[AchFilesResponse]:
        with get_db_connection(row_factory=dict_row) as conn:
            result = conn.execute(
                """
WITH exceptions AS (
                    SELECT DISTINCT(afe.ach_files_id)
                    FROM ach_exceptions AS afe
)
SELECT af.ach_files_id AS id,
                       af.file_name AS filename,
                       af.created_at AS date,    
                       afh.immediate_origin_name AS originator,                 
                       afcr.total_debit_entry_dollar_amount AS debit_total, 
                       afcr.total_credit_entry_dollar_amount AS credit_total,
                      CASE
                         WHEN exceptions.ach_files_id IS NOT NULL THEN TRUE
                         ELSE FALSE
                      END AS has_exceptions
                FROM ach_files AS af
                INNER JOIN ach_records_type_1 AS art1 USING (ach_files_id)
                INNER JOIN ach_records_type_9 AS art9 USING (ach_records_type_1_id)
                LEFT JOIN ach_file_headers AS afh USING (ach_records_type_1_id)
                LEFT JOIN ach_file_control_details AS afcr USING (ach_records_type_9_id) 
                LEFT JOIN exceptions USING (ach_files_id)
                ORDER BY af.created_at DESC
                LIMIT %s
                OFFSET %s                
                """,
                [limit, offset],
            )

            return result.fetchall()

    @staticmethod
    def get_batches(ach_file_id: UUID) -> list[AchBatchesResponse]:
        with get_db_connection(row_factory=dict_row) as conn:
            result = conn.execute(
                """
                    SELECT COALESCE(abh.company_name, '') AS company_name,
                           COALESCE(abh.company_identification, aibh.originating_dfi_identification) AS company_id,
                           art5.ach_records_type_5_id AS id,
                           COALESCE(abh.batch_number, aibh.batch_number) AS batch_number,
                           abcd.total_debit_entry_dollar_amount AS debit_total,
                           abcd.total_credit_entry_dollar_amount AS credit_total, 
                           abcd.entry_addenda_count 
                      FROM ach_files AS af
                INNER JOIN ach_records_type_1 AS art1 USING (ach_files_id)
                INNER JOIN ach_records_type_5 AS art5 USING (ach_records_type_1_id)
                INNER JOIN ach_records_type_8 AS art8 USING (ach_records_type_5_id)
                INNER JOIN ach_batch_control_details AS abcd USING (ach_records_type_8_id)
                LEFT JOIN ach_batch_headers AS abh USING (ach_records_type_5_id)
                LEFT JOIN ach_iat_batch_headers AS aibh USING (ach_records_type_5_id)
                     WHERE af.ach_files_id = %s
                  ORDER BY COALESCE(abh.originating_dfi_identification, aibh.originating_dfi_identification);
                """,
                [ach_file_id.hex],
            )

            return result.fetchall()

    @staticmethod
    def get_entries(
        ach_file_id: UUID, ach_batch_id: UUID
    ) -> list[AchBatchEntriesResponse]:
        if AchFileSql._is_iat_batch(ach_file_id, ach_batch_id):
            return AchFileSql._get_iat_entries(ach_file_id, ach_batch_id)
        else:
            return AchFileSql._get_ppd_entries(ach_file_id, ach_batch_id)

    @staticmethod
    def _is_iat_batch(ach_file_id: UUID, ach_batch_id: UUID):
        with get_db_connection(row_factory=dict_row) as conn:
            result = conn.execute(
                """
                SELECT COUNT(1) > 0 AS is_iat
                FROM ach_files AS af
                INNER JOIN ach_records_type_1 AS art1 USING (ach_files_id)
                INNER JOIN ach_records_type_5 AS art5 USING (ach_records_type_1_id)
                INNER JOIN ach_records_type_6 AS art6 USING (ach_records_type_5_id)
                INNER JOIN ach_iat_entry_details AS aied USING (ach_records_type_6_id)
                WHERE af.ach_files_id = %s
                AND art5.ach_records_type_5_id = %s
                """,
                [ach_file_id.hex, ach_batch_id.hex],
            )

            return result.fetchone()["is_iat"]

    @staticmethod
    def _get_iat_entries(
        ach_file_id: UUID, ach_batch_id: UUID
    ) -> list[AchBatchEntriesResponse]:
        with get_db_connection(row_factory=dict_row) as conn:
            result = conn.execute(
                """
                WITH addenda_records_for_entry AS (
                   SELECT art6.ach_records_type_6_id,
                   COUNT(art7.*) AS addenda_count
                   FROM ach_files AS af
                   INNER JOIN ach_records_type_1 AS art1 USING (ach_files_id)
                   INNER JOIN ach_records_type_5 AS art5 USING (ach_records_type_1_id)
                   INNER JOIN ach_records_type_6 AS art6 USING (ach_records_type_5_id)
                   INNER JOIN ach_iat_entry_details AS aped USING (ach_records_type_6_id)
                   LEFT JOIN ach_records_type_7 AS art7 USING (ach_records_type_6_id)
                   WHERE af.ach_files_id = %s
                   AND art5.ach_records_type_5_id = %s
                   GROUP BY (art6.ach_records_type_6_id)
                   )
                   SELECT art6.ach_records_type_6_id AS id,
                   aied.transaction_code,
                   CASE
                     WHEN aied.transaction_code IN (21, 31, 41, 26, 36, 46) THEN 'NOC'
                     WHEN aied.transaction_code IN (22, 32, 42 ) THEN 'Credit'
                     WHEN aied.transaction_code IN (23, 33, 43, 28, 38, 48) THEN 'Prenotification'
                     WHEN aied.transaction_code IN (27, 37, 47) THEN 'Debit'
                     WHEN aied.transaction_code IN (24, 34, 44, 29, 39, 49) THEN 'Zero dollar with remittance'
                     ELSE 'Unknown'
                   END AS transaction_description,
                   CASE
                     WHEN aied.transaction_code IN (31, 32, 33, 34, 36, 37, 38, 39) THEN 'Savings'
                     WHEN aied.transaction_code IN (21, 22, 23, 24, 26, 27, 28, 29) THEN 'Checking'
                     WHEN aied.transaction_code IN (41, 42, 43, 46, 47, 48) THEN 'GL'
                     WHEN aied.transaction_code IN (51, 52, 53, 55, 56 ) THEN 'Loan'
                     ELSE 'Unknown'
                   END AS application,
                   aia10d.receiving_name AS individual_name,
                   aied.amount,
                   CONCAT(
                      '*************',
                      RIGHT(LPAD(aied.foreign_receivers_account_number, 4, '0'), 4)
                   ) AS account_number_last_4,
                   arfe.addenda_count
                   FROM ach_files AS af
                   INNER JOIN ach_records_type_1 AS art1 USING (ach_files_id)
                   INNER JOIN ach_records_type_5 AS art5 USING (ach_records_type_1_id)
                   INNER JOIN ach_records_type_6 AS art6 USING (ach_records_type_5_id)
                   INNER JOIN ach_records_type_7 AS art7 USING (ach_records_type_6_id)
                   INNER JOIN ach_iat_entry_details AS aied USING (ach_records_type_6_id)
                   INNER JOIN addenda_records_for_entry AS arfe USING (ach_records_type_6_id)
                   INNER JOIN ach_iat_addenda_10_details AS aia10d USING (ach_records_type_7_id)
                   WHERE af.ach_files_id = %s
                   AND art5.ach_records_type_5_id = %s
                """,
                [ach_file_id.hex, ach_batch_id.hex, ach_file_id.hex, ach_batch_id.hex],
            )
            return result.fetchall()

    @staticmethod
    def _get_ppd_entries(
        ach_file_id: UUID, ach_batch_id: UUID
    ) -> list[AchBatchEntriesResponse]:
        with get_db_connection(row_factory=dict_row) as conn:
            result = conn.execute(
                """
                WITH addenda_records_for_entry AS (
                   SELECT art6.ach_records_type_6_id,
                   COUNT(art7.*) AS addenda_count
                   FROM ach_files AS af
                   INNER JOIN ach_records_type_1 AS art1 USING (ach_files_id)
                   INNER JOIN ach_records_type_5 AS art5 USING (ach_records_type_1_id)
                   INNER JOIN ach_records_type_6 AS art6 USING (ach_records_type_5_id)
                   INNER JOIN ach_ppd_entry_details AS aped USING (ach_records_type_6_id)
                   LEFT JOIN ach_records_type_7 AS art7 USING (ach_records_type_6_id)
                   WHERE af.ach_files_id = %s
                   AND art5.ach_records_type_5_id = %s
                   GROUP BY (art6.ach_records_type_6_id)
                   )
                   SELECT art6.ach_records_type_6_id AS id,
                   aped.transaction_code, 
                   CASE 
                     WHEN aped.transaction_code IN (21, 31, 41, 26, 36, 46) THEN 'NOC'
                     WHEN aped.transaction_code IN (22, 32, 42 ) THEN 'Credit'
                     WHEN aped.transaction_code IN (23, 33, 43, 28, 38, 48) THEN 'Prenotification'
                     WHEN aped.transaction_code IN (27, 37, 47) THEN 'Debit'
                     WHEN aped.transaction_code IN (24, 34, 44, 29, 39, 49) THEN 'Zero dollar with remittance'
                     ELSE 'Unknown'
                   END AS transaction_description,
                   CASE 
                     WHEN aped.transaction_code IN (31, 32, 33, 34, 36, 37, 38, 39) THEN 'Savings'
                     WHEN aped.transaction_code IN (21, 22, 23, 24, 26, 27, 28, 29) THEN 'Checking'
                     WHEN aped.transaction_code IN (41, 42, 43, 46, 47, 48) THEN 'GL'
                     WHEN aped.transaction_code IN (51, 52, 53, 55, 56 ) THEN 'Loan'
                     ELSE 'Unknown'
                   END AS application,                   
                   aped.individual_name,
                   aped.amount, 
                   CONCAT( 
                      '*************',
                      RIGHT(LPAD(aped.dfi_account_number, 4, '0'), 4)
                   ) AS account_number_last_4, 
                   arfe.addenda_count
                   FROM ach_files AS af
                   INNER JOIN ach_records_type_1 AS art1 USING (ach_files_id)
                   INNER JOIN ach_records_type_5 AS art5 USING (ach_records_type_1_id)
                   INNER JOIN ach_records_type_6 AS art6 USING (ach_records_type_5_id)
                   INNER JOIN ach_ppd_entry_details AS aped USING (ach_records_type_6_id)
                   INNER JOIN addenda_records_for_entry AS arfe USING (ach_records_type_6_id)
                   WHERE af.ach_files_id = %s
                   AND art5.ach_records_type_5_id = %s
                """,
                [ach_file_id.hex, ach_batch_id.hex, ach_file_id.hex, ach_batch_id.hex],
            )
            return result.fetchall()

    @staticmethod
    def get_record(ach_file_id: UUID) -> AchFileSchema:
        with get_db_connection(row_factory=class_row(AchFileSchema)) as conn:
            result = conn.execute(
                """
                SELECT * FROM ach_files WHERE ach_files_id = %s
                """,
                [ach_file_id.hex],
            )

            record = result.fetchone()

            if not record:
                raise KeyError(f"Record with id {ach_file_id} not found")

            return record
