import os
from typing import List
from uuid import UUID

import psycopg

from chapter6.AchProcessor_V3.ach_processor.database.ach_addenda_ppd_sql import AchAddendaPpdSql
from chapter6.AchProcessor_V3.ach_processor.database.ach_batch_control_sql import AchBatchControlSql
from chapter6.AchProcessor_V3.ach_processor.database.ach_batch_header_sql import AchBatchHeaderSql
from chapter6.AchProcessor_V3.ach_processor.database.ach_entry_ppd_details_sql import AchEntryPpdDetailsSql
from chapter6.AchProcessor_V3.ach_processor.database.ach_file_control_sql import AchFileControlSql
from chapter6.AchProcessor_V3.ach_processor.database.ach_file_header_sql import AchFileHeaderSql
from chapter6.AchProcessor_V3.ach_processor.database.ach_records_sql import AchRecordsSql
from chapter6.AchProcessor_V3.ach_processor.schemas.ach_addenda_ppd_schema import AchAddendaPpdSchema
from chapter6.AchProcessor_V3.ach_processor.schemas.ach_batch_control_schema import AchBatchControlSchema
from chapter6.AchProcessor_V3.ach_processor.schemas.ach_batch_header_schema import AchBatchHeaderSchema
from chapter6.AchProcessor_V3.ach_processor.schemas.ach_entry_ppd_details_schema import AchEntryPpdDetailsSchema
from chapter6.AchProcessor_V3.ach_processor.schemas.ach_file_control_schema import AchFileControlSchema
from chapter6.AchProcessor_V3.ach_processor.schemas.ach_file_header_schema import AchFileHeaderSchema
from chapter6.AchProcessor_V3.ach_processor.schemas.ach_record_schema import AchRecordSchema


class AchFileProcessor:
    last_trace_number = None
    expected_record_types = ["1"]
    POSTGRES_USER = "someuser"
    POSTGRES_PASSWORD = "supersecret"

    DATABASE_URL = f"dbname={POSTGRES_USER} user={POSTGRES_USER} password={POSTGRES_PASSWORD} host=localhost port=5432"

    def __init__(self):
        self.expected_record_types = ["1"]
        self.last_trace_number = None

    def get_db(self):
        conn = psycopg.connect(self.DATABASE_URL)
        return conn

    def parse(self, ach_file_id, filename) -> [List, List]:

        with open(filename, "r") as file, self.get_db() as conn:
            lines = file.readlines()
            sequence_number = 0
            current_file_header_id = None
            current_batch_header_id = None
            current_entry_id = None

            for line in lines:
                sequence_number += 1
                line = line.replace("\n", "")

                ach_record = AchRecordSchema(
                    ach_files_id=ach_file_id,
                    file_name=os.path.basename(filename),
                    unparsed_record=line,
                    sequence_number=sequence_number
                )

                ach_record_id = AchRecordsSql().insert_record(ach_record)

                if len(line) != 94:
                    self._add_exception("Invalid line length")
                    continue

                record_type = line[0]

                if record_type not in self.expected_record_types:
                    # Reset expected record types, so we do not get multiple errors
                    self.expected_record_types = ["5", "6", "7", "8", "9"]
                    self._add_exception("Unexpected record type")
                    continue

                match record_type:
                    case "1":
                        self._parse_file_header(ach_record_id, line)
                        current_file_header_id = ach_record_id
                    case "5":
                        self._parse_batch_header(ach_record_id, current_file_header_id, line)
                        current_batch_header_id = ach_record_id
                    case "6":
                        self._parse_entry_ppd_detail(ach_record_id, current_batch_header_id, line)
                        current_entry_id = ach_record_id
                    case "7":
                        self._parse_addenda_ppd(ach_record_id, current_entry_id, line)
                    case "8":
                        self.last_trace_number = None
                        self._parse_batch_control(ach_record_id, current_batch_header_id, line)
                    case "9":
                        self._parse_file_control(ach_record_id, current_file_header_id, line)
                    case _:
                        self._add_exception(f"Unknown record type: {record_type}")

    def _parse_file_header(self,
                           ach_record_id: UUID,
                           line: str):
        self.expected_record_types = ["5"]

        ach_file_header = AchFileHeaderSchema(
            ach_records_id=ach_record_id,
            record_type_code=line[0],
            priority_code=line[1:3],
            immediate_destination=line[3:13].strip(),
            immediate_origin=line[13:23].strip(),
            file_creation_date=line[23:29],
            file_creation_time=line[29:33],
            file_id_modifier=line[33],
            record_size=line[34:37],
            blocking_factor=line[37:39],
            format_code=line[39],
            immediate_destination_name=line[40:63].strip(),
            immediate_origin_name=line[63:86].strip(),
            reference_code=line[86:94].strip(),
        )

        AchFileHeaderSql().insert_record(ach_file_header)

    def _parse_batch_header(self,
                            ach_record_id: UUID,
                            current_file_header_id: UUID,
                            line: str):
        self.expected_record_types = ["6"]

        ach_batch_header = AchBatchHeaderSchema(
            ach_records_id=ach_record_id,
            ach_file_headers_id=current_file_header_id,
            record_type_code=line[0],
            service_class_code=line[1:4],
            company_name=line[4:20].strip(),
            company_discretionary_data=line[20:40].strip(),
            company_identification=line[40:50].strip(),
            standard_entry_class_code=line[50:53],
            company_entry_description=line[53:63].strip(),
            company_descriptive_date=line[63:69],
            effective_entry_date=line[69:75],
            settlement_date=line[75:78],
            originator_status_code=line[78],
            originating_dfi_identification=line[79:86],
            batch_number=line[87:94]
        )

        AchBatchHeaderSql().insert_record(ach_batch_header)

    def _parse_entry_ppd_detail(self,
                                ach_record_id: UUID,
                                current_batch_header_id: UUID,
                                line: str):

        ach_entry_ppd_detail_record = AchEntryPpdDetailsSchema(
            ach_records_id=ach_record_id,
            ach_batch_headers_id=current_batch_header_id,
            record_type_code=line[0],
            transaction_code=line[1:3],
            receiving_dfi_identification=line[3:11],
            check_digit=line[11],
            dfi_account_number=line[12:29].strip(),
            amount=line[29:39],
            individual_identification_number=line[39:54].strip(),
            individual_name=line[54:76].strip(),
            discretionary_data=line[76:78].strip(),
            addenda_record_indicator=line[78],
            trace_number=line[79:94],
        )

        AchEntryPpdDetailsSql().insert_record(ach_entry_ppd_detail_record)

        if ach_entry_ppd_detail_record.addenda_record_indicator == "1":
            self.expected_record_types = ["7"]
        else:
            self.expected_record_types = ["6", "8"]

        if (
                self.last_trace_number is None
                or ach_entry_ppd_detail_record.trace_number > self.last_trace_number
        ):
            self.last_trace_number = ach_entry_ppd_detail_record.trace_number
        else:
            self._add_exception("Trace number out of order")

    def _parse_addenda_ppd(self,
                           ach_record_id: UUID,
                           current_entry_id: UUID,
                           line: str):
        self.expected_record_types = ["6", "7", "8"]

        addenda_ppd_record = AchAddendaPpdSchema(
            ach_records_id=ach_record_id,
            ach_entry_ppd_details_id=current_entry_id,
            record_type_code=line[0],
            addenda_type_code=line[1:3],
            payment_related_information=line[3:83].strip(),
            addenda_sequence_number=line[83:87],
            entry_detail_sequence_number=line[87:94],
        )

        AchAddendaPpdSql().insert_record(addenda_ppd_record)

    def _parse_batch_control(self,
                             ach_record_id: UUID,
                             current_batch_header_id: UUID,
                             line: str):
        self.expected_record_types = ["5", "9"]

        batch_control_record = AchBatchControlSchema(
            ach_records_id=ach_record_id,
            ach_batch_headers_id=current_batch_header_id,
            record_type_code=line[0],
            service_class_code=line[1:4],
            entry_addenda_count=line[4:10],
            entry_hash=line[10:20].strip(),
            total_debit_entry_dollar_amount=line[20:32],
            total_credit_entry_dollar_amount=line[32:44],
            company_identification=line[44:54].strip(),
            message_authentication_code=line[54:73].strip(),
            reserved=line[73:79].strip(),
            originating_dfi_identification=line[79:87],
            batch_number=line[87:94],
        )

        AchBatchControlSql().insert_record(batch_control_record)

    def _parse_file_control(self,
                            ach_record_id: UUID,
                            current_file_header_id: UUID,
                            line: str):
        self.expected_record_types = ["9"]

        file_control_record = AchFileControlSchema(
            ach_records_id=ach_record_id,
            ach_file_headers_id=current_file_header_id,
            record_type_code=line[0],
            batch_count=line[1:7],
            block_count=line[7:13],
            entry_addenda_count=line[13:21],
            entry_hash=line[21:31].strip(),
            total_debit_entry_dollar_amount=line[31:43],
            total_credit_entry_dollar_amount=line[43:55],
            reserved=line[55:94],
        )

        AchFileControlSql().insert_record(file_control_record)

    def _add_exception(self, exception: str) -> None:
        with self.get_db() as conn:
            conn.execute("""
        INSERT INTO ach_exceptions (ach_exceptions_id, exception_description)
                     VALUES (DEFAULT, %(exception)s)
                     """, {"exception": exception})
