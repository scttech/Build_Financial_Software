from enum import Enum


class AchExceptions(Enum):
    INVALID_LINE_LENGTH = "001"
    UNEXPECTED_RECORD_TYPE = "002"
    TRACE_NUMBER_OUT_OF_ORDER = "003"
    INVALID_FILE_ID_MODIFIER = "004"
    INVALID_IMMEDIATE_DESTINATION = "005"
    COMPANY_LIMITS_EXCEEDED = "006"
