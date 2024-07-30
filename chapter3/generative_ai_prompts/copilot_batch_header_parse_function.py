from typing import Dict


def _parse_batch_header(self, line: str) -> Dict[str, str]:
    return {
        "record_type_code": line[0],
        "service_class_code": line[1:4],
        "company_name": line[4:20].strip(),
        "company_discretionary_data": line[20:40].strip(),
        "company_identification": line[40:50].strip(),
        "standard_entry_class_code": line[50:53],
        "company_entry_description": line[53:63].strip(),
        "company_descriptive_date": line[63:68],
        "effective_entry_date": line[68:74],
        "settlement_date": line[74:80],
        "originator_status_code": line[80],
        "originating_dfi_id": line[81:89],
        "batch_number": line[89:94],
    }
