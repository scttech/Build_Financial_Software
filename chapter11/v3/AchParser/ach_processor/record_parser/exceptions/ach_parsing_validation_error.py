from typing import Any

from chapter11.v3.AchParser.ach_processor.ach_exceptions import AchExceptions


class AchParsingValidationError(Exception):
    """Exception raised for errors parsing the ACH records.

    Attributes:
        message -- explanation of the error
    """

    def __init__(
        self, message: str = "Error parsing ACH record", validation_errors: Any = None
    ):
        self.message = message
        self.validation_errors = validation_errors
        super().__init__(message)

    def get_exception_codes(self) -> list[str]:
        exception_codes = []
        for error in self.validation_errors:
            if error["loc"][0] == "file_id_modifier":
                exception_codes.append(AchExceptions.INVALID_FILE_ID_MODIFIER.value)
            elif error["loc"][0] == "immediate_destination":
                exception_codes.append(
                    AchExceptions.INVALID_IMMEDIATE_DESTINATION.value
                )
        return exception_codes
