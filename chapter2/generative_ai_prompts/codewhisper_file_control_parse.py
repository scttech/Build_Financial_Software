# Define a function to parse a Nacha Type 9 record
from typing import Dict


def parse_type_9(line: str) -> Dict[str, str]:
    return {
        "record_type_code": line[0],
        "service_class_code": line[3:6],
        "standard_entry_class_code": line[6:9],
        "transaction_code": line[9],
        "receiving_dfi_identification": line[10:20].strip(),
        "receiving_dfi_account_number": line[20:30].strip(),
        "amount": line[30:38],
        "individual_identification_number": line[38:55].strip(),
        "individual_name": line[55:76].strip(),
        "discretionary_data": line[76:78].strip(),
        "addenda_record_indicator": line[78],
        "trace_number": line[79:94].strip(),
        "sequence_number": line[94:97].strip(),
        "entry_detail_sequence_number": line[97:98].strip(),
        "addenda_sequence_number": line[98:99].strip(),
        "addenda_type_code": line[99:100].strip(),
        "addenda_information": line[100:].strip(),
        "addenda_count": line[2:4].strip(),
        "entry_hash": line[4:20].strip(),
        "batch_number": line[20:24].strip(),
        "block_count": line[24:28].strip(),
        "entry_addenda_count": line[28:32].strip(),
        "originating_dfi_identification": line[32:40].strip(),
        "originating_dfi_account_number": line[40:54].strip(),
        "trace_number_modifier": line[54:55].strip(),
        "trace_number_check_digit": line[55:56].strip(),
    }