from typing import List
from uuid import UUID

from chapter12.v3.AchParser.ach_processor.ach_exceptions import AchExceptions
from chapter12.v3.AchParser.ach_processor.database.ach.iat.ach_iat_710_addenda_sql import (
    AchIat710AddendaSql,
)
from chapter12.v3.AchParser.ach_processor.database.ach.iat.ach_iat_711_addenda_sql import (
    AchIat711AddendaSql,
)
from chapter12.v3.AchParser.ach_processor.database.ach.iat.ach_iat_712_addenda_sql import (
    AchIat712AddendaSql,
)
from chapter12.v3.AchParser.ach_processor.database.ach.iat.ach_iat_713_addenda_sql import (
    AchIat713AddendaSql,
)
from chapter12.v3.AchParser.ach_processor.database.ach.iat.ach_iat_714_addenda_sql import (
    AchIat714AddendaSql,
)
from chapter12.v3.AchParser.ach_processor.database.ach.iat.ach_iat_715_addenda_sql import (
    AchIat715AddendaSql,
)
from chapter12.v3.AchParser.ach_processor.database.ach.iat.ach_iat_716_addenda_sql import (
    AchIat716AddendaSql,
)
from chapter12.v3.AchParser.ach_processor.database.ach.iat.ach_iat_batch_header_sql import (
    AchIatBatchHeaderSql,
)
from chapter12.v3.AchParser.ach_processor.database.ach.iat.ach_iat_entry_details_sql import (
    AchIatEntryDetailsSql,
)
from chapter12.v3.AchParser.ach_processor.database.ach_addenda_ppd_sql import (
    AchAddendaPpdSql,
)
from chapter12.v3.AchParser.ach_processor.database.ach_batch_control_sql import (
    AchBatchControlSql,
)
from chapter12.v3.AchParser.ach_processor.database.ach_batch_header_sql import (
    AchBatchHeaderSql,
)
from chapter12.v3.AchParser.ach_processor.database.ach_entry_ppd_details_sql import (
    AchEntryPpdDetailsSql,
)
from chapter12.v3.AchParser.ach_processor.database.ach_file_control_sql import (
    AchFileControlSql,
)
from chapter12.v3.AchParser.ach_processor.database.ach_file_header_sql import (
    AchFileHeaderSql,
)
from chapter12.v3.AchParser.ach_processor.database.ach_records_sql_type_1 import (
    AchRecordsSqlType1,
)
from chapter12.v3.AchParser.ach_processor.database.ach_records_sql_type_5 import (
    AchRecordsSqlType5,
)
from chapter12.v3.AchParser.ach_processor.database.ach_records_sql_type_6 import (
    AchRecordsSqlType6,
)
from chapter12.v3.AchParser.ach_processor.database.ach_records_sql_type_7 import (
    AchRecordsSqlType7,
)
from chapter12.v3.AchParser.ach_processor.database.ach_records_sql_type_8 import (
    AchRecordsSqlType8,
)
from chapter12.v3.AchParser.ach_processor.database.ach_records_sql_type_9 import (
    AchRecordsSqlType9,
)
from chapter12.v3.AchParser.ach_processor.database.ach_records_sql_type_invalid import (
    AchRecordsSqlTypeInvalid,
)
from chapter12.v3.AchParser.ach_processor.database.exception.ach_exceptions_sql import (
    AchExceptionsSql,
)
from chapter12.v3.AchParser.ach_processor.record_parser.ach_record_parser import (
    AchRecordProcessor,
)
from chapter12.v3.AchParser.ach_processor.record_parser.exceptions.ach_parsing_validation_error import (
    AchParsingValidationError,
)
from chapter12.v3.AchParser.ach_processor.schemas.database.ach_record.ach_record_type_1_schema import (
    AchRecordType1Schema,
)
from chapter12.v3.AchParser.ach_processor.schemas.database.ach_record.ach_record_type_5_schema import (
    AchRecordType5Schema,
)
from chapter12.v3.AchParser.ach_processor.schemas.database.ach_record.ach_record_type_6_schema import (
    AchRecordType6Schema,
)
from chapter12.v3.AchParser.ach_processor.schemas.database.ach_record.ach_record_type_7_schema import (
    AchRecordType7Schema,
)
from chapter12.v3.AchParser.ach_processor.schemas.database.ach_record.ach_record_type_8_schema import (
    AchRecordType8Schema,
)
from chapter12.v3.AchParser.ach_processor.schemas.database.ach_record.ach_record_type_9_schema import (
    AchRecordType9Schema,
)
from chapter12.v3.AchParser.ach_processor.schemas.database.ach_record.ach_record_type_invalid_schema import (
    AchRecordTypeInvalidSchema,
)
from chapter12.v3.AchParser.ach_processor.schemas.database.exception.ach_exception_schema import (
    AchExceptionSchema,
)
from chapter12.v3.AchParser.common.database.company.company_limits_sql import (
    CompanyLimitsSql,
)


class AchFileProcessor:
    last_trace_number = None
    expected_record_types = ["1"]
    expected_addenda_type = ""
    batch_type = ""

    def __init__(self):
        self.expected_record_types = ["1"]
        self.batch_type = ""
        self.last_trace_number = None
        self.expected_addenda_type = ""

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
                        if line[50:53] == "IAT":
                            self._parse_iat_batch_header(ach_record_id, line)
                            self.batch_type = "IAT"
                        elif line[50:53] == "PPD":
                            self._parse_batch_header(ach_record_id, line)
                            self.batch_type = "PPD"
                        else:
                            self._add_exception(
                                AchExceptionSchema(
                                    ach_files_id=ach_file_id,
                                    record_number=sequence_number,
                                    exception_code=AchExceptions.INVALID_SEC.value,
                                ),
                                line,
                            )
                        current_batch_header_id = ach_record_id
                    case "6":
                        ach_record = AchRecordType6Schema(
                            ach_records_type_5_id=current_batch_header_id,
                            unparsed_record=line,
                            sequence_number=sequence_number,
                        )
                        ach_record_id = AchRecordsSqlType6().insert_record(ach_record)
                        if self.batch_type == "IAT":
                            self.expected_addenda_type = "10"
                            self._parse_iat_entry_detail(
                                ach_file_id=ach_file_id,
                                current_batch_header_id=current_batch_header_id,
                                ach_records_type_6_id=ach_record_id,
                                sequence_number=sequence_number,
                                line=line,
                            )
                        elif self.batch_type == "PPD":
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

                        if self.batch_type == "IAT":
                            self._parse_iat_addenda(
                                ach_record_id, line, sequence_number
                            )
                        elif self.batch_type == "PPD":
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
                        if CompanyLimitsSql().file_exceeds_company_limits(ach_file_id):
                            AchExceptionsSql().insert_record(
                                AchExceptionSchema(
                                    ach_files_id=ach_file_id,
                                    ach_batch_id=current_batch_header_id,
                                    record_number=sequence_number,
                                    exception_code=AchExceptions.COMPANY_LIMITS_EXCEEDED.value,
                                )
                            )
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

    def _parse_iat_batch_header(self, ach_records_type_5_id: UUID, line: str):
        self.expected_record_types = ["6"]

        ach_iat_batch_header = AchRecordProcessor().parse_iat_batch_header(
            ach_records_type_5_id, line
        )
        AchIatBatchHeaderSql().insert_record(ach_iat_batch_header)

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

    def _parse_iat_addenda(
        self, ach_records_type_7_id: UUID, line: str, sequence_number
    ):
        addenda_type = line[1:3]

        if addenda_type != self.expected_addenda_type:
            print(
                f"Unexpected addenda type: {addenda_type} expected: {self.expected_addenda_type}"
            )
            self._add_exception(
                AchExceptionSchema(
                    ach_files_id=ach_records_type_7_id,
                    record_number=sequence_number,
                    exception_code=AchExceptions.UNEXPECTED_ADDENDA_TYPE.value,
                )
            )
            return

        if addenda_type == "10":
            self._parse_iat_addenda_710(ach_records_type_7_id, line)
        elif addenda_type == "11":
            self._parse_iat_addenda_711(ach_records_type_7_id, line)
        elif addenda_type == "12":
            self._parse_iat_addenda_712(ach_records_type_7_id, line)
        elif addenda_type == "13":
            self._parse_iat_addenda_713(ach_records_type_7_id, line)
        elif addenda_type == "14":
            self._parse_iat_addenda_714(ach_records_type_7_id, line)
        elif addenda_type == "15":
            self._parse_iat_addenda_715(ach_records_type_7_id, line)
        elif addenda_type == "16":
            self._parse_iat_addenda_716(ach_records_type_7_id, line)
        else:
            self._add_exception(
                AchExceptionSchema(
                    ach_files_id=ach_records_type_7_id,
                    record_number=sequence_number,
                    exception_code=AchExceptions.INVALID_IAT_ADDENDA_TYPE.value,
                )
            )

    def _parse_iat_addenda_710(self, ach_records_type_7_id: UUID, line: str):
        self.expected_record_types = ["7"]
        self.expected_addenda_type = "11"

        ach_iat_addenda_record = AchRecordProcessor().parse_iat_addenda_710(
            ach_records_type_7_id, line
        )
        AchIat710AddendaSql().insert_record(ach_iat_addenda_record)

    def _parse_iat_addenda_711(self, ach_records_type_7_id: UUID, line: str):
        self.expected_record_types = ["7"]
        self.expected_addenda_type = "12"

        ach_iat_addenda_record = AchRecordProcessor().parse_iat_addenda_711(
            ach_records_type_7_id, line
        )
        AchIat711AddendaSql().insert_record(ach_iat_addenda_record)

    def _parse_iat_addenda_712(self, ach_records_type_7_id: UUID, line: str):
        self.expected_record_types = ["7"]
        self.expected_addenda_type = "13"

        ach_iat_addenda_record = AchRecordProcessor().parse_iat_addenda_712(
            ach_records_type_7_id, line
        )
        AchIat712AddendaSql().insert_record(ach_iat_addenda_record)

    def _parse_iat_addenda_713(self, ach_records_type_7_id: UUID, line: str):
        self.expected_record_types = ["7"]
        self.expected_addenda_type = "14"

        ach_iat_addenda_record = AchRecordProcessor().parse_iat_addenda_713(
            ach_records_type_7_id, line
        )
        AchIat713AddendaSql().insert_record(ach_iat_addenda_record)

    def _parse_iat_addenda_714(self, ach_records_type_7_id: UUID, line: str):
        self.expected_record_types = ["7"]
        self.expected_addenda_type = "15"

        ach_iat_addenda_record = AchRecordProcessor().parse_iat_addenda_714(
            ach_records_type_7_id, line
        )
        AchIat714AddendaSql().insert_record(ach_iat_addenda_record)

    def _parse_iat_addenda_715(self, ach_records_type_7_id: UUID, line: str):
        self.expected_record_types = ["7"]
        self.expected_addenda_type = "16"

        ach_iat_addenda_record = AchRecordProcessor().parse_iat_addenda_715(
            ach_records_type_7_id, line
        )
        AchIat715AddendaSql().insert_record(ach_iat_addenda_record)

    def _parse_iat_addenda_716(self, ach_records_type_7_id: UUID, line: str):
        self.expected_record_types = ["6", "7", "8"]
        self.expected_addenda_type = ""

        ach_iat_addenda_record = AchRecordProcessor().parse_iat_addenda_716(
            ach_records_type_7_id, line
        )
        AchIat716AddendaSql().insert_record(ach_iat_addenda_record)

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

    def _parse_iat_entry_detail(
        self,
        ach_file_id: UUID,
        current_batch_header_id: UUID,
        ach_records_type_6_id: UUID,
        sequence_number: int,
        line: str,
    ):
        ach_iat_entry_detail_record = AchRecordProcessor().parse_iat_entry_detail(
            ach_records_type_6_id, line
        )
        AchIatEntryDetailsSql().insert_record(ach_iat_entry_detail_record)

        if ach_iat_entry_detail_record.addenda_record_indicator == "1":
            self.expected_record_types = ["7"]
        else:
            self.expected_record_types = ["6", "8"]

        if (
            self.last_trace_number is None
            or ach_iat_entry_detail_record.trace_number > self.last_trace_number
        ):
            self.last_trace_number = ach_iat_entry_detail_record.trace_number
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
