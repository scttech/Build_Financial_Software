# Write a class to parse an ACH file for each NACHA record type and return a list of transactions

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
                    self.transactions.append(ACHBatchHeader(line))
                elif line.startswith('5'):
                    self.transactions.append(ACHBatchControl(line))
                elif line.startswith('6'):
                    self.transactions.append(ACHEntryDetail(line))
                elif line.startswith('7'):
                    self.transactions.append(ACHAddendaRecord(line))
                elif line.startswith('8'):
                    self.transactions.append(ACHFileControl(line))
                else:
                    raise ValueError('Invalid ACH record type')

    def get_transactions(self):
        return self.transactions

# Write a class to parse an ACH file
