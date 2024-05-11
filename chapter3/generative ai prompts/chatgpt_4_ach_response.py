def parse_ach(filename):
    records = []

    with open(filename, 'r') as file:
        lines = file.readlines()

        for line in lines:
            record_type = line[0]

            if record_type == '1':  # File Header Record
                record = {
                    'record_type': 'File Header',
                    'priority_code': line[1:3],
                    'immediate_destination': line[3:13],
                    'immediate_origin': line[13:23],
                    # ... additional fields
                }

            elif record_type == '5':  # Batch Header Record
                record = {
                    'record_type': 'Batch Header',
                    'service_class_code': line[1:4],
                    'company_name': line[4:20],
                    # ... additional fields
                }

            elif record_type == '6':  # Entry Detail Record
                record = {
                    'record_type': 'Entry Detail',
                    'transaction_code': line[1:3],
                    'receiving_dfi_id': line[3:11],
                    'account_number': line[12:29],
                    'amount': line[29:39],
                    # ... additional fields
                }

            elif record_type == '7':  # Addenda Record
                record = {
                    'record_type': 'Addenda',
                    # ... additional fields based on the specific addenda type
                }

            elif record_type == '8':  # Batch Control Record
                record = {
                    'record_type': 'Batch Control',
                    # ... additional fields
                }

            elif record_type == '9':  # File Control Record
                record = {
                    'record_type': 'File Control',
                    # ... additional fields
                }

            else:
                print(f"Unknown record type: {record_type} in line: {line}")
                continue

            records.append(record)

    return records


# Test the function with an ACH file
parsed_records = parse_ach('path_to_ach_file.txt')
for record in parsed_records:
    print(record)
