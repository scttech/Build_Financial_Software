from chapter3.ACH_Parser_v2.ach_processor.AchFileProcessor import AchFileProcessor


def test_parse_entry_detail():
    # Define a sample ACH batch header record
    sample_addenda_record = "705Test 2                                                                          00020003001"

    # Define the expected result of parsing the sample ACH entry detail record
    expected_result = {
        "record_type_code": "7",
        "addenda_type_code": "05",
        "payment_related_information": "Test 2",
        "addenda_sequence_number": "0002",
        "entry_detail_sequence_number": "0003001",
    }

    parser = AchFileProcessor()

    result = parser._parse_addenda(sample_addenda_record)

    assert result == expected_result, f"Expected {expected_result}, but got {result}"
