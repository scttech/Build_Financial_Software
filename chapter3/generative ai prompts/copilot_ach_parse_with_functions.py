# Write a class to parse an ACH file with separate functions for each NACHA record type and return a list of transactions
def ACHFileControl(line):
    # Temp function just to clear error within IDE
    pass


def ACHBatchHeader(line):
    # Temp function just to clear error within IDE
    pass


def ACHBatchControl(line):
    # Temp function just to clear error within IDE
    pass


def ACHEntryDetail(line):
    # Temp function just to clear error within IDE
    pass


def ACHAddendaRecord(line):
    # Temp function just to clear error within IDE
    pass

class ACHParser:
    def __init__(self, ach_file):
        self.ach_file = ach_file
        self.transactions = []
        self.parse_ach_file()

    def parse_ach_file(self):
        with open(self.ach_file, 'r') as f:
            for line in f:
                if line.startswith('1'):
                    self.transactions.append(self.parse_ach_batch_header(line))
                elif line.startswith('5'):
                    self.transactions.append(self.parse_ach_batch_control(line))
                elif line.startswith('6'):
                    self.transactions.append(self.parse_ach_entry_detail(line))
                elif line.startswith('7'):
                    self.transactions.append(self.parse_ach_addenda_record(line))
                elif line.startswith('8'):
                    self.transactions.append(self.parse_ach_file_control(line))
                else:
                    raise ValueError('Invalid ACH record type')

    def parse_ach_batch_header(self, line):
        return ACHBatchHeader(line)

    def parse_ach_batch_control(self, line):
        return ACHBatchControl(line)

    def parse_ach_entry_detail(self, line):
        return ACHEntryDetail(line)

    def parse_ach_addenda_record(self, line):
        return ACHAddendaRecord(line)

    def parse_ach_file_control(self, line):
        return ACHFileControl(line)

    def get_transactions(self):
        return self.transactions
