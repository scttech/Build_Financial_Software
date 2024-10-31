from chapter2.v3.ach_processor.AchFileProcessor import AchFileProcessor


def test_parse_entry_detail():
    # Define a sample ACH batch header record
    sample_entry_detail_record = "6272670841345                0000000301               0003xxxxxxxxxxxxxxxx  LC1061000010003001"

    # Define the expected result of parsing the sample ACH entry detail record
    expected_result = {
        "record_type_code": "6",
        "transaction_code": "27",
        "receiving_dfi_identification": "26708413",
        "check_digit": "4",
        "dfi_account_number": "5",
        "amount": "0000000301",
        "individual_identification_number": "",
        "individual_name": "0003xxxxxxxxxxxxxxxx",
        "discretionary_data": "LC",
        "addenda_record_indicator": "1",
        "trace_number": "061000010003001",
    }

    parser = AchFileProcessor()

    result = parser._parse_entry_detail(sample_entry_detail_record)

    assert result == expected_result, f"Expected {expected_result}, but got {result}"
