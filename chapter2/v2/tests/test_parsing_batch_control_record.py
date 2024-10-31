from chapter2.v2.ach_processor.AchFileProcessor import AchFileProcessor


def test_parse_batch_control():
    # Define a sample batch control record
    sample_batch_control_record = "82000000080016501650000000000301000000000302CompID                             061000010000003"

    # Define the expected result of parsing the batch control record
    expected_result = {
        "record_type_code": "8",
        "service_class_code": "200",
        "entry_addenda_count": "000008",
        "entry_hash": "0016501650",
        "total_debit_entry_dollar_amount": "000000000301",
        "total_credit_entry_dollar_amount": "000000000302",
        "company_identification": "CompID",
        "message_authentication_code": "",
        "reserved": "",
        "originating_dfi_identification": "06100001",
        "batch_number": "0000003",
    }

    parser = AchFileProcessor()

    result = parser._parse_batch_control(sample_batch_control_record)

    assert result == expected_result, f"Expected {expected_result}, but got {result}"
