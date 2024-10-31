import os
from typing import Dict, List, Any

import psycopg
from psycopg import Connection


class AchFileProcessor:
    records = []
    last_trace_number = None
    expected_record_types = ["1"]
    POSTGRES_USER = "someuser"
    POSTGRES_PASSWORD = "supersecret"

    DATABASE_URL = f"dbname={POSTGRES_USER} user={POSTGRES_USER} password={POSTGRES_PASSWORD} host=localhost port=5432"
    def __init__(self):
        self.records = []
        self.expected_record_types = ["1"]
        self.last_trace_number = None

    def get_db(self):
        conn = psycopg.connect(self.DATABASE_URL)
        return conn

    def parse(self, filename) -> [List, List]:

        with open(filename, "r") as file, self.get_db() as conn:
            lines = file.readlines()
            sequence_number = 0

            for line in lines:
                sequence_number += 1
                line = line.replace("\n", "")

                conn.execute(f"INSERT INTO ach_files (file_name, unparsed_record, sequence_number) VALUES (%s, %s, %s)", (os.path.basename(filename), line, sequence_number))

                if len(line) != 94:
                    self._add_exception(conn, "Invalid line length")
                    continue

                record_type = line[0]

                if record_type not in self.expected_record_types:
                    # Reset expected record types, so we do not get multiple errors
                    self.expected_record_types = ["5", "6", "7", "8", "9"]
                    self._add_exception(conn, "Unexpected record type")
                    continue

                match record_type:
                    case "1":
                        result = self._parse_file_header(conn, line)
                    case "5":
                        result = self._parse_batch_header(conn, line)
                    case "6":
                        result = self._parse_entry_ppd_detail(conn, line)
                    case "7":
                        result = self._parse_addenda_ppd(conn, line)
                    case "8":
                        self.last_trace_number = None
                        result = self._parse_batch_control(conn, line)
                    case "9":
                        result = self._parse_file_control(conn, line)
                    case _:
                        result = None
                        self._add_exception(conn, f"Unknown record type: {record_type}")

                self.records.append(result)

        return self.records

    def _parse_file_header(self, conn: Connection[tuple[Any, ...]], line: str) -> Dict[str, str]:
        self.expected_record_types = ["5"]

        file_header = {
            "record_type_code": line[0],
            "priority_code": line[1:3],
            "immediate_destination": line[3:13].strip(),
            "immediate_origin": line[13:23].strip(),
            "file_creation_date": line[23:29],
            "file_creation_time": line[29:33],
            "file_id_modifier": line[33],
            "record_size": line[34:37],
            "blocking_factor": line[37:39],
            "format_code": line[39],
            "immediate_destination_name": line[40:63].strip(),
            "immediate_origin_name": line[63:86].strip(),
            "reference_code": line[86:94].strip(),
        }

        conn.execute(f"INSERT INTO ach_file_headers (ach_file_headers_id, "
                           f"record_type_code, priority_code, immediate_destination, immediate_origin,"
                           f"file_creation_date, file_creation_time, file_id_modifier, record_size,"
                           f"blocking_factor, format_code, immediate_destination_name,"
                           f"immediate_origin_name, reference_code) "
                           f"VALUES (DEFAULT, %(record_type_code)s, %(priority_code)s, %(immediate_destination)s, "
                           f"%(immediate_origin)s, %(file_creation_date)s, %(file_creation_time)s, "
                            f"%(file_id_modifier)s, %(record_size)s, %(blocking_factor)s, %(format_code)s, "
                            f"%(immediate_destination_name)s, %(immediate_origin_name)s, %(reference_code)s)"
                           , file_header)

        return file_header

    def _parse_batch_header(self, conn: Connection[tuple[Any, ...]], line: str) -> Dict[str, str]:
        self.expected_record_types = ["6"]

        batch_header = {
            "record_type_code": line[0],
            "service_class_code": line[1:4],
            "company_name": line[4:20].strip(),
            "company_discretionary_data": line[20:40].strip(),
            "company_identification": line[40:50].strip(),
            "standard_entry_class_code": line[50:53],
            "company_entry_description": line[53:63].strip(),
            "company_descriptive_date": line[63:69],
            "effective_entry_date": line[69:75],
            "settlement_date": line[75:78],
            "originator_status_code": line[78],
            "originating_dfi_identification": line[79:86],
            "batch_number": line[87:94],
        }

        conn.execute(
            f"INSERT INTO ach_batch_headers (ach_batch_headers_id, record_type_code, service_class_code, company_name, "
            f"company_discretionary_data, company_identification, standard_entry_class_code, company_entry_description, "
            f"company_descriptive_date, effective_entry_date, settlement_date, originator_status_code, "
            f"originating_dfi_identification, batch_number) "
            f"VALUES (DEFAULT, %(record_type_code)s, %(service_class_code)s, %(company_name)s, "
            f"%(company_discretionary_data)s, %(company_identification)s, %(standard_entry_class_code)s, "
            f"%(company_entry_description)s, %(company_descriptive_date)s, %(effective_entry_date)s, "
            f"%(settlement_date)s, %(originator_status_code)s, %(originating_dfi_identification)s, "
            f"%(batch_number)s)", batch_header
        )

        return batch_header

    def _parse_entry_ppd_detail(self, conn: Connection[tuple[Any, ...]], line: str) -> Dict[str, str]:
        entry_detail_ppd_record = {
            "record_type_code": line[0],
            "transaction_code": line[1:3],
            "receiving_dfi_identification": line[3:11],
            "check_digit": line[11],
            "dfi_account_number": line[12:29].strip(),
            "amount": line[29:39],
            "individual_identification_number": line[39:54].strip(),
            "individual_name": line[54:76].strip(),
            "discretionary_data": line[76:78].strip(),
            "addenda_record_indicator": line[78],
            "trace_number": line[79:94],
        }

        conn.execute(
            f"INSERT INTO ach_entry_ppd_details (ach_entry_ppd_details_id, record_type_code, transaction_code, "
            f"receiving_dfi_identification, check_digit, dfi_account_number, amount, "
            f"individual_identification_number, individual_name, discretionary_data, "
            f"addenda_record_indicator, trace_number) "
            f"VALUES (DEFAULT, %(record_type_code)s, %(transaction_code)s, %(receiving_dfi_identification)s, "
            f"%(check_digit)s, %(dfi_account_number)s, %(amount)s, %(individual_identification_number)s, "
            f"%(individual_name)s, %(discretionary_data)s, %(addenda_record_indicator)s, %(trace_number)s)",
            entry_detail_ppd_record
        )

        if entry_detail_ppd_record["addenda_record_indicator"] == "1":
            self.expected_record_types = ["7"]
        else:
            self.expected_record_types = ["6", "8"]

        if (
            self.last_trace_number is None
            or entry_detail_ppd_record["trace_number"] > self.last_trace_number
        ):
            self.last_trace_number = entry_detail_ppd_record["trace_number"]
        else:
            self._add_exception(conn, "Trace number out of order")
            return {"Trace number out of order": line}

        return entry_detail_ppd_record

    def _parse_addenda_ppd(self, conn: Connection[tuple[Any, ...]], line: str) -> Dict[str, str]:
        self.expected_record_types = ["6", "7", "8"]

        addenda_ppd_record = {
            "record_type_code": line[0],
            "addenda_type_code": line[1:3],
            "payment_related_information": line[3:83].strip(),
            "addenda_sequence_number": line[83:87],
            "entry_detail_sequence_number": line[87:94],
        }

        conn.execute(
            f"INSERT INTO ach_addenda_ppd_records (ach_addenda_ppd_records_id, record_type_code, addenda_type_code, "
            f"payment_related_information, addenda_sequence_number, entry_detail_sequence_number) "
            f"VALUES (DEFAULT, %(record_type_code)s, %(addenda_type_code)s, %(payment_related_information)s, "
            f"%(addenda_sequence_number)s, %(entry_detail_sequence_number)s)",
            addenda_ppd_record
        )

        return addenda_ppd_record

    def _parse_batch_control(self, conn: Connection[tuple[Any, ...]], line: str) -> Dict[str, str]:
        self.expected_record_types = ["5", "9"]

        batch_control_record = {
            "record_type_code": line[0],
            "service_class_code": line[1:4],
            "entry_addenda_count": line[4:10],
            "entry_hash": line[10:20].strip(),
            "total_debit_entry_dollar_amount": line[20:32],
            "total_credit_entry_dollar_amount": line[32:44],
            "company_identification": line[44:54].strip(),
            "message_authentication_code": line[54:73].strip(),
            "reserved": line[73:79].strip(),
            "originating_dfi_identification": line[79:87],
            "batch_number": line[87:94],
        }

        conn.execute(
            f"INSERT INTO ach_batch_control_records (ach_batch_control_records_id, record_type_code, "
            f"service_class_code, entry_addenda_count, entry_hash, total_debit_entry_dollar_amount, "
            f"total_credit_entry_dollar_amount, company_identification, message_authentication_code, "
            f"reserved, originating_dfi_identification, batch_number) "
        f"VALUES (DEFAULT, %(record_type_code)s, %(service_class_code)s, %(entry_addenda_count)s, "
            f"%(entry_hash)s, %(total_debit_entry_dollar_amount)s, %(total_credit_entry_dollar_amount)s, "
            f"%(company_identification)s, %(message_authentication_code)s, %(reserved)s, "
            f"%(originating_dfi_identification)s, %(batch_number)s)",
            batch_control_record
        )

        return batch_control_record

    def _parse_file_control(self, conn: Connection[tuple[Any, ...]], line: str) -> Dict[str, str]:
        self.expected_record_types = ["9"]

        file_control_record = {
            "record_type_code": line[0],
            "batch_count": line[1:7],
            "block_count": line[7:13],
            "entry_addenda_count": line[13:21],
            "entry_hash": line[21:31].strip(),
            "total_debit_entry_dollar_amount": line[31:43],
            "total_credit_entry_dollar_amount": line[43:55],
            "reserved": line[55:94],
        }

        conn.execute(
            f"INSERT INTO ach_file_control_records (ach_file_control_records_id, record_type_code, batch_count, "
            f"block_count, entry_addenda_count, entry_hash, total_debit_entry_dollar_amount, "
            f"total_credit_entry_dollar_amount, reserved) "
            f"VALUES (DEFAULT, %(record_type_code)s, %(batch_count)s, %(block_count)s, "
            f"%(entry_addenda_count)s, %(entry_hash)s, %(total_debit_entry_dollar_amount)s, "
            f"%(total_credit_entry_dollar_amount)s, %(reserved)s)",
            file_control_record
        )

        return file_control_record

    def _add_exception(self, conn: Connection[tuple[Any, ...]], exception: str) -> None:
        conn.execute(f"INSERT INTO ach_exceptions (ach_exceptions_id, exception_description) "
                     f"VALUES (DEFAULT, %(exception)s)", {"exception": exception} )
        return
