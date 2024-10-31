from chapter2.v3.ach_processor.AchFileProcessor import AchFileProcessor


# Define a test function to test parsing an ACH batch header record using AchFileProcessor._parse_batch_header()
def test_parse_batch_header():
    # Define a sample ACH batch header record
    sample_batch_header = "5200Company name    DiscretionaryData   Company IDARCComp desc 0216232302160471061000010000001"

    # Define the expected result of parsing the sample ACH batch header record
    expected_result = {
        "record_type_code": "5",
        "service_class_code": "200",
        "company_name": "Company name",
        "company_discretionary_data": "DiscretionaryData",
        "company_identification": "Company ID",
        "standard_entry_class_code": "ARC",
        "company_entry_description": "Comp desc",
        "company_descriptive_date": "021623",
        "effective_entry_date": "230216",
        "settlement_date": "047",
        "originator_status_code": "1",
        "originating_dfi_identification": "0610000",
        "batch_number": "0000001",
    }

    # Create an instance of AchFileProcessor
    parser = AchFileProcessor()

    # Call AchFileProcessor._parse_batch_header() with the sample ACH batch header record
    result = parser._parse_batch_header(sample_batch_header)

    # Assert that the result of parsing the sample ACH batch header record matches the expected result
    assert result == expected_result, f"Expected {expected_result}, but got {result}"
