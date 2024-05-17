from chapter3.ACH_Parser_v1.ach_processor.AchFileProcessor import AchFileProcessor


def test_parse_file_header():
    sample_header = "101 267084131 6910001340402200830A094101DEST NAME              ORIGIN NAME            XXXXXXXX"

    expected_result = {
        "record_type_code": "1",
        "priority_code": "01",
        "immediate_destination": "267084131",
        "immediate_origin": "691000134",
        "file_creation_date": "040220",
        "file_creation_time": "0830",
        "file_id_modifier": "A",
        "record_size": "094",
        "blocking_factor": "10",
        "format_code": "1",
        "immediate_destination_name": "DEST NAME",
        "immediate_origin_name": "ORIGIN NAME",
        "reference_code": "XXXXXXXX",
    }

    parser = AchFileProcessor()
    result = parser._parse_file_header(sample_header)
    assert result == expected_result, f"Expected {expected_result}, but got {result}"
