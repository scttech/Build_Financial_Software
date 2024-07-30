from typing import Dict, List


class AchFileProcessor:
    records = []

    def parse(self, filename) -> List[Dict[str, str]]:
        parser_functions = {
            "1": self._parse_file_header,
            "5": self._parse_batch_header,
            "6": self._parse_entry_detail,
            "7": self._parse_addenda,
            "8": self._parse_batch_control,
            "9": self._parse_file_control,
        }

        with open(filename, "r") as file:
            lines = file.readlines()

            for line in lines:
                record_type = line[0]
                parser = parser_functions.get(record_type)

                if parser:
                    self.records.append(parser(line))
                else:
                    print(f"Unknown record type: {record_type} in line: {line}")

        return self.records

    def _parse_file_header(self, line: str) -> Dict[str, str]:
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

    # ... Other parsing functions ...

    def _parse_batch_header(self, line: str) -> Dict[str, str]:
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
        # Your implementation here
        pass

    def _parse_addenda(self, line: str) -> Dict[str, str]:
        # Your implementation here
        pass

    def _parse_batch_control(self, line: str) -> Dict[str, str]:
        # Your implementation here
        pass

    def _parse_file_control(self, line: str) -> Dict[str, str]:
        # Your implementation here
        pass
