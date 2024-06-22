from typing import List
from uuid import UUID

from chapter11.v3.AchParser.ach_processor.ach_exceptions import AchExceptions
from chapter11.v3.AchParser.ach_processor.database.ach_addenda_ppd_sql import (
    AchAddendaPpdSql,
)
from chapter11.v3.AchParser.ach_processor.database.ach_batch_control_sql import (
    AchBatchControlSql,
)
from chapter11.v3.AchParser.ach_processor.database.ach_batch_header_sql import (
    AchBatchHeaderSql,
)
from chapter11.v3.AchParser.ach_processor.database.ach_entry_ppd_details_sql import (
    AchEntryPpdDetailsSql,
)
from chapter11.v3.AchParser.ach_processor.database.ach_file_control_sql import (
    AchFileControlSql,
)
from chapter11.v3.AchParser.ach_processor.database.ach_file_header_sql import (
    AchFileHeaderSql,
)
from chapter11.v3.AchParser.ach_processor.database.ach_records_sql_type_1 import (
    AchRecordsSqlType1,
)
from chapter11.v3.AchParser.ach_processor.database.ach_records_sql_type_5 import (
    AchRecordsSqlType5,
)
from chapter11.v3.AchParser.ach_processor.database.ach_records_sql_type_6 import (
    AchRecordsSqlType6,
)
from chapter11.v3.AchParser.ach_processor.database.ach_records_sql_type_7 import (
    AchRecordsSqlType7,
)
from chapter11.v3.AchParser.ach_processor.database.ach_records_sql_type_8 import (
    AchRecordsSqlType8,
)
from chapter11.v3.AchParser.ach_processor.database.ach_records_sql_type_9 import (
    AchRecordsSqlType9,
)
from chapter11.v3.AchParser.ach_processor.database.ach_records_sql_type_invalid import (
    AchRecordsSqlTypeInvalid,
)
from chapter11.v3.AchParser.ach_processor.database.exception.ach_exceptions_sql import (
    AchExceptionsSql,
)
from chapter11.v3.AchParser.ach_processor.record_parser.ach_record_parser import (
    AchRecordProcessor,
)
from chapter11.v3.AchParser.ach_processor.record_parser.exceptions.ach_parsing_validation_error import (
    AchParsingValidationError,
)
from chapter11.v3.AchParser.ach_processor.schemas.database.ach_record.ach_record_type_1_schema import (
    AchRecordType1Schema,
)
from chapter11.v3.AchParser.ach_processor.schemas.database.ach_record.ach_record_type_5_schema import (
    AchRecordType5Schema,
)
from chapter11.v3.AchParser.ach_processor.schemas.database.ach_record.ach_record_type_6_schema import (
    AchRecordType6Schema,
)
from chapter11.v3.AchParser.ach_processor.schemas.database.ach_record.ach_record_type_7_schema import (
    AchRecordType7Schema,
)
from chapter11.v3.AchParser.ach_processor.schemas.database.ach_record.ach_record_type_8_schema import (
    AchRecordType8Schema,
)
from chapter11.v3.AchParser.ach_processor.schemas.database.ach_record.ach_record_type_9_schema import (
    AchRecordType9Schema,
)
from chapter11.v3.AchParser.ach_processor.schemas.database.ach_record.ach_record_type_invalid_schema import (
    AchRecordTypeInvalidSchema,
)
from chapter11.v3.AchParser.ach_processor.schemas.database.exception.ach_exception_schema import (
    AchExceptionSchema,
)


class AchFileProcessor:
    last_trace_number = None
    expected_record_types = ["1"]

    def __init__(self):
        self.expected_record_types = ["1"]
        self.last_trace_number = None

    def parse(self, ach_file_id, filename) -> [List, List]:

        with open(filename, "r", encoding="utf8") as file:
            print(f"Processing file: {filename}")
            lines = file.readlines()
            sequence_number = 0
            current_file_header_id = None
            current_batch_header_id = None
            current_entry_id = None
            print(f"Processing {len(lines)} lines")

            for line in lines:
                print(f"Processing line: {line}")
                sequence_number += 1
                line = line.replace("\n", "")

                if len(line) != 94:
                    self.expected_record_types = ["5", "6", "7", "8", "9"]
                    self._add_exception(
                        AchExceptionSchema(
                            ach_files_id=ach_file_id,
                            record_number=sequence_number,
                            exception_code=AchExceptions.INVALID_LINE_LENGTH.value,
                        ),
                        line,
                    )
                    continue

                record_type = line[0]

                if record_type not in self.expected_record_types:
                    # Reset expected record types, so we do not get multiple errors
                    self.expected_record_types = ["5", "6", "7", "8", "9"]
                    self._add_exception(
                        AchExceptionSchema(
                            ach_files_id=ach_file_id,
                            record_number=sequence_number,
                            exception_code=AchExceptions.UNEXPECTED_RECORD_TYPE.value,
                        ),
                        line,
                    )
                    continue

                match record_type:
                    case "1":
                        ach_record = AchRecordType1Schema(
                            ach_files_id=ach_file_id,
                            unparsed_record=line,
                            sequence_number=sequence_number,
                        )
                        ach_record_id = AchRecordsSqlType1().insert_record(ach_record)
                        current_file_header_id = ach_record_id
                        try:
                            self._parse_file_header(ach_record_id, line)
                        except AchParsingValidationError as e:
                            for exception_code in e.get_exception_codes():
                                self._add_exception(
                                    AchExceptionSchema(
                                        ach_files_id=ach_file_id,
                                        record_number=sequence_number,
                                        exception_code=exception_code,
                                    )
                                )
                    case "5":
                        ach_record = AchRecordType5Schema(
                            ach_records_type_1_id=current_file_header_id,
                            unparsed_record=line,
                            sequence_number=sequence_number,
                        )
                        ach_record_id = AchRecordsSqlType5().insert_record(ach_record)
                        self._parse_batch_header(ach_record_id, line)
                        current_batch_header_id = ach_record_id
                    case "6":
                        ach_record = AchRecordType6Schema(
                            ach_records_type_5_id=current_batch_header_id,
                            unparsed_record=line,
                            sequence_number=sequence_number,
                        )
                        ach_record_id = AchRecordsSqlType6().insert_record(ach_record)
                        self._parse_entry_ppd_detail(
                            ach_file_id=ach_file_id,
                            current_batch_header_id=current_batch_header_id,
                            ach_records_type_6_id=ach_record_id,
                            sequence_number=sequence_number,
                            line=line,
                        )
                        current_entry_id = ach_record_id
                    case "7":
                        ach_record = AchRecordType7Schema(
                            ach_records_type_6_id=current_entry_id,
                            unparsed_record=line,
                            sequence_number=sequence_number,
                        )
                        ach_record_id = AchRecordsSqlType7().insert_record(ach_record)
                        self._parse_addenda_ppd(ach_record_id, line)
                    case "8":
                        ach_record = AchRecordType8Schema(
                            ach_records_type_5_id=current_batch_header_id,
                            unparsed_record=line,
                            sequence_number=sequence_number,
                        )
                        ach_record_id = AchRecordsSqlType8().insert_record(ach_record)
                        self.last_trace_number = None
                        self._parse_batch_control(ach_record_id, line)
                    case "9":
                        ach_record = AchRecordType9Schema(
                            ach_records_type_1_id=current_file_header_id,
                            unparsed_record=line,
                            sequence_number=sequence_number,
                        )
                        ach_record_id = AchRecordsSqlType9().insert_record(ach_record)
                        self._parse_file_control(ach_record_id, line)
                    case _:
                        self._add_exception(
                            AchExceptionSchema(
                                ach_files_id=ach_file_id,
                                record_number=sequence_number,
                                exception_code=AchExceptions.UNEXPECTED_RECORD_TYPE.value,
                            ),
                            line,
                        )
        print(f"Finished processing file: {filename}")
        return sequence_number

    def _parse_file_header(self, ach_records_type_1_id: UUID, line: str):
        self.expected_record_types = ["5"]

        ach_file_header = AchRecordProcessor().parse_file_header(
            ach_records_type_1_id, line
        )
        AchFileHeaderSql().insert_record(ach_file_header)

    def _parse_batch_header(self, ach_records_type_5_id: UUID, line: str):
        self.expected_record_types = ["6"]

        ach_batch_header = AchRecordProcessor().parse_batch_header(
            ach_records_type_5_id, line
        )
        AchBatchHeaderSql().insert_record(ach_batch_header)

    def _parse_entry_ppd_detail(
        self,
        ach_file_id: UUID,
        current_batch_header_id: UUID,
        ach_records_type_6_id: UUID,
        sequence_number: int,
        line: str,
    ):
        ach_entry_ppd_detail_record = AchRecordProcessor().parse_entry_ppd_detail(
            ach_records_type_6_id, line
        )
        AchEntryPpdDetailsSql().insert_record(ach_entry_ppd_detail_record)

        if ach_entry_ppd_detail_record.addenda_record_indicator == "1":
            self.expected_record_types = ["7"]
        else:
            self.expected_record_types = ["6", "8"]

        if (
            self.last_trace_number is None
            or ach_entry_ppd_detail_record.trace_number > self.last_trace_number
        ):
            self.last_trace_number = ach_entry_ppd_detail_record.trace_number
        else:
            self._add_exception(
                AchExceptionSchema(
                    ach_files_id=ach_file_id,
                    ach_batch_id=current_batch_header_id,
                    ach_entry_id=ach_records_type_6_id,
                    record_number=sequence_number,
                    exception_code=AchExceptions.TRACE_NUMBER_OUT_OF_ORDER.value,
                )
            )

    def _parse_addenda_ppd(self, ach_records_type_7_id: UUID, line: str):
        self.expected_record_types = ["6", "7", "8"]

        addenda_ppd_record = AchRecordProcessor().parse_addenda_ppd(
            ach_records_type_7_id, line
        )
        AchAddendaPpdSql().insert_record(addenda_ppd_record)

    def _parse_batch_control(self, ach_records_type_8_id: UUID, line: str):
        self.expected_record_types = ["5", "9"]

        batch_control_record = AchRecordProcessor().parse_batch_control(
            ach_records_type_8_id, line
        )
        AchBatchControlSql().insert_record(batch_control_record)

    def _parse_file_control(self, ach_records_type_9_id: UUID, line: str):
        self.expected_record_types = ["9"]

        file_control_record = AchRecordProcessor().parse_file_control(
            ach_records_type_9_id, line
        )
        AchFileControlSql().insert_record(file_control_record)

    @staticmethod
    def _add_exception(exception: AchExceptionSchema, line=None) -> None:
        sql = AchExceptionsSql()
        sql.insert_record(exception)
        if line is not None:
            sql_invalid_rec = AchRecordsSqlTypeInvalid()
            sql_invalid_rec.insert_record(
                AchRecordTypeInvalidSchema(
                    ach_files_id=exception.ach_files_id,
                    unparsed_record=line,
                    sequence_number=exception.record_number,
                )
            )
