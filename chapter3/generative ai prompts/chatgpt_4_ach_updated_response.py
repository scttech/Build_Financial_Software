def parse_file_header(line):
    return {
        'record_type': 'File Header',
        'priority_code': line[1:3],
        'immediate_destination': line[3:13],
        'immediate_origin': line[13:23],
        # ... additional fields
    }

def parse_batch_header(line):
    return {
        'record_type': 'Batch Header',
        'service_class_code': line[1:4],
        'company_name': line[4:20],
        # ... additional fields
    }

def parse_entry_detail(line):
    return {
        'record_type': 'Entry Detail',
        'transaction_code': line[1:3],
        'receiving_dfi_id': line[3:11],
        'account_number': line[12:29],
        'amount': line[29:39],
        # ... additional fields
    }

def parse_addenda(line):
    return {
        'record_type': 'Addenda',
        # ... additional fields based on the specific addenda type
    }

def parse_batch_control(line):
    return {
        'record_type': 'Batch Control',
        # ... additional fields
    }

def parse_file_control(line):
    return {
        'record_type': 'File Control',
        # ... additional fields
    }

def parse_ach(filename):
    records = []

    parser_functions = {
        '1': parse_file_header,
        '5': parse_batch_header,
        '6': parse_entry_detail,
        '7': parse_addenda,
        '8': parse_batch_control,
        '9': parse_file_control
    }

    with open(filename, 'r') as file:
        lines = file.readlines()

        for line in lines:
            record_type = line[0]
            parser = parser_functions.get(record_type)

            if parser:
                records.append(parser(line))
            else:
                print(f"Unknown record type: {record_type} in line: {line}")
                continue

    return records


# Test the function with an ACH file
parsed_records = parse_ach('path_to_ach_file.txt')
for record in parsed_records:
    print(record)
