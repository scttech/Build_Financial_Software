from typing import Dict


def _parse_batch_control(self, line: str) -> Dict[str, str]:
    return {
        "record_type_code": line[0],
        "service_class_code": line[1:4],
        "entry_hash": line[4:14].strip(),
        "total_number_of_entries": line[14:18],
    }
