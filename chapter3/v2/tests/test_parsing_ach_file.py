from chapter3.v2.ach_processor.AchFileProcessor import AchFileProcessor


def test_record_count():
    expected_result = 41
    parser = AchFileProcessor()
    result = parser.parse("data/sample.ach")
    assert (
        len(result) == expected_result
    ), f"Expected {expected_result}, but got {len(result)}"
