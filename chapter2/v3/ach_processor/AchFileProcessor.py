from typing import Dict, List


class AchFileProcessor:
    records = []
    exceptions = []
    last_trace_number = None
    expected_record_types = ["1"]

    def __init__(self):
        self.records = []
        self.exceptions = []
        self.expected_record_types = ["1"]
        self.last_trace_number = None

    def parse(self, filename) -> [List, List]:
        with open(filename, "r") as file:
            lines = file.readlines()

            for line in lines:
                line = line.replace("\n", "")

                if len(line) != 94:
                    self.exceptions.append("Invalid line length")
                    self.records.append({"Invalid line length": line})
                    continue

                record_type = line[0]

                if record_type not in self.expected_record_types:
                    # Reset expected record types, so we do not get multiple errors
                    self.expected_record_types = ["5", "6", "7", "8", "9"]
                    self.exceptions.append("Unexpected record type")
                    self.records.append({"Unexpected record type": line})
                    continue

                match record_type:
                    case "1":
                        result = self._parse_file_header(line)
                    case "5":
                        result = self._parse_batch_header(line)
                    case "6":
                        result = self._parse_entry_detail(line)
                    case "7":
                        result = self._parse_addenda(line)
                    case "8":
                        self.last_trace_number = None
                        result = self._parse_batch_control(line)
                    case "9":
                        result = self._parse_file_control(line)
                    case _:
                        result = None
                        print(f"Unknown record type:  {line}")

                self.records.append(result)

        return self.records, self.exceptions

    def _parse_file_header(self, line: str) -> Dict[str, str]:
        self.expected_record_types = ["5"]

        return {
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

    def _parse_batch_header(self, line: str) -> Dict[str, str]:
        self.expected_record_types = ["6"]

        return {
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

    def _parse_entry_detail(self, line: str) -> Dict[str, str]:
        entry_detail_record = {
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

        if entry_detail_record["addenda_record_indicator"] == "1":
            self.expected_record_types = ["7"]
        else:
            self.expected_record_types = ["6", "8"]

        if (
            self.last_trace_number is None
            or entry_detail_record["trace_number"] > self.last_trace_number
        ):
            self.last_trace_number = entry_detail_record["trace_number"]
        else:
            self.exceptions.append("Trace number out of order")
            return {"Trace number out of order": line}

        return entry_detail_record

    def _parse_addenda(self, line: str) -> Dict[str, str]:
        self.expected_record_types = ["6", "7", "8"]

        return {
            "record_type_code": line[0],
            "addenda_type_code": line[1:3],
            "payment_related_information": line[3:83].strip(),
            "addenda_sequence_number": line[83:87],
            "entry_detail_sequence_number": line[87:94],
        }

    def _parse_batch_control(self, line: str) -> Dict[str, str]:
        self.expected_record_types = ["5", "9"]

        return {
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

    def _parse_file_control(self, line: str) -> Dict[str, str]:
        self.expected_record_types = ["9"]

        return {
            "record_type_code": line[0],
            "batch_count": line[1:7],
            "block_count": line[7:13],
            "entry_addenda_count": line[13:21],
            "entry_hash": line[21:31].strip(),
            "total_debit_entry_dollar_amount": line[31:43],
            "total_credit_entry_dollar_amount": line[43:55],
            "reserved": line[55:94],
        }
