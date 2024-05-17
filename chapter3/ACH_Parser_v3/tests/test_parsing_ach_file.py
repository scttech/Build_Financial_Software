import os

from chapter3.ACH_Parser_v3.ach_processor.AchFileProcessor import AchFileProcessor


def test_record_count():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(dir_path, "data", "sample.ach")
    expected_result = 41
    parser = AchFileProcessor()
    records, exceptions = parser.parse(file_path)
    assert (
        len(records) == expected_result
    ), f"Expected {expected_result}, but got {len(records)}"
