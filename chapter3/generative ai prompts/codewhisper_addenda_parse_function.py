from typing import Dict


def _parse_addenda(self, line: str) -> Dict[str, str]:
    return {
        "record_type_code": line[0],
        "addenda_sequence_number": line[1:3],
        "service_class_code": line[3:6],
        "addenda_type_code": line[6],
    }
