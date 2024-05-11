class ACHParser:
    def __init__(self, ach_file_path):
        self.ach_file_path = ach_file_path
        self.records = []

    def parse(self):
        with open(self.ach_file_path, 'r') as file:
            lines = file.readlines()

        record_type = None
        current_record = {}

        for line in lines:
            record_code = line[0]
            if record_code == '1':
                record_type = 'header'
            elif record_code == '6':
                record_type = 'batch'
            elif record_code == '7':
                record_type = 'entry'
            elif record_code == '9':
                record_type = 'footer'

            if record_type:
                current_record[record_type] = line.strip()
                if record_type == 'footer':
                    self.records.append(current_record)
                    current_record = {}
                    record_type = None

    def get_records(self):
        return self.records


if __name__ == "__main__":
    ach_file_path = "example.ach"
    parser = ACHParser(ach_file_path)
    parser.parse()

    records = parser.get_records()
    for record in records:
        print(record)
