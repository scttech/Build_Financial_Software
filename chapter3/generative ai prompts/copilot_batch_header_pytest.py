# Define a test function to test parsing an ACH batch header record using AchFileProcessor._parse_batch_header()
def test_parse_batch_header():
    # Define a sample ACH batch header record
    sample_batch_header = "5225Sample Company Name          Sample Company Discretionary DataSample Company IdentificationPPDCompany Entry DescriptionSample Company Descriptive DateSample Effective Entry Date"

    # Define the expected result of parsing the sample ACH batch header record
    expected_result = {
        "record_type_code": "5",
        "service_class_code": "225",
        "company_name": "Sample Company Name",
        "company_discretionary_data": "Sample Company Discretionary Data",
        "company_identification": "Sample Company Identification",
        "standard_entry_class_code": "PPD",
        "company_entry_description": "Company Entry Description",
        "company_descriptive_date": "Sample Company Descriptive Date",
        "effective_entry_date": "Sample Effective Entry Date",
    }

    # Create an instance of AchFileProcessor
    parser = AchFileProcessor()

    # Call AchFileProcessor._parse_batch_header() with the sample ACH batch header record
    result = parser._parse_batch_header(sample_batch_header)

    # Assert that the result of parsing the sample ACH batch header record matches the expected result
    assert result == expected_result, f"Expected {expected_result}, but got {result}"