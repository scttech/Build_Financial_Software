from decimal import Decimal
from uuid import UUID

from pydantic import ValidationError

from chapter10.AchParserV1.ach_processor.record_parser.exceptions.ach_parsing_validation_error import AchParsingValidationError
from chapter10.AchParserV1.ach_processor.schemas.database.ach_addenda_ppd_schema import AchAddendaPpdSchema
from chapter10.AchParserV1.ach_processor.schemas.database.ach_batch_control_schema import (
    AchBatchControlSchema,
)
from chapter10.AchParserV1.ach_processor.schemas.database.ach_batch_header_schema import AchBatchHeaderSchema
from chapter10.AchParserV1.ach_processor.schemas.database.ach_entry_ppd_details_schema import (
    AchEntryPpdDetailsSchema,
)
from chapter10.AchParserV1.ach_processor.schemas.database.ach_file_control_schema import AchFileControlSchema
from chapter10.AchParserV1.ach_processor.schemas.database.ach_file_header_schema import AchFileHeaderSchema


class AchRecordProcessor:
    @staticmethod
    def parse_file_header(
            ach_records_type_1_id: UUID, record: str
    ) -> AchFileHeaderSchema:
        try:
            return AchFileHeaderSchema(
                ach_records_type_1_id=ach_records_type_1_id,
                record_type_code=record[0],
                priority_code=record[1:3],
                immediate_destination=record[3:13].strip(),
                immediate_origin=record[13:23].strip(),
                file_creation_date=record[23:29],
                file_creation_time=record[29:33],
                file_id_modifier=record[33],
                record_size=record[34:37],
                blocking_factor=record[37:39],
                format_code=record[39],
                immediate_destination_name=record[40:63].strip(),
                immediate_origin_name=record[63:86].strip(),
                reference_code=record[86:94].strip(),
            )
        except ValidationError as e:
            raise AchParsingValidationError(message='Error parsing file header', validation_errors=e.errors())

    @staticmethod
    def parse_batch_header(
            ach_records_type_5_id: UUID, record: str
    ) -> AchBatchHeaderSchema:
        return AchBatchHeaderSchema(
            ach_records_type_5_id=ach_records_type_5_id,
            record_type_code=record[0],
            service_class_code=record[1:4],
            company_name=record[4:20].strip(),
            company_discretionary_data=record[20:40].strip(),
            company_identification=record[40:50].strip(),
            standard_entry_class_code=record[50:53],
            company_entry_description=record[53:63].strip(),
            company_descriptive_date=record[63:69],
            effective_entry_date=record[69:75],
            settlement_date=record[75:78],
            originator_status_code=record[78],
            originating_dfi_identification=record[79:86],
            batch_number=record[87:94],
        )

    @staticmethod
    def parse_entry_ppd_detail(
            ach_records_type_6_id: UUID, record: str
    ) -> AchEntryPpdDetailsSchema:
        return AchEntryPpdDetailsSchema(
            ach_records_type_6_id=ach_records_type_6_id,
            record_type_code=record[0],
            transaction_code=record[1:3],
            receiving_dfi_identification=record[3:11],
            check_digit=record[11],
            dfi_account_number=record[12:29].strip(),
            amount=Decimal(f"{record[29:37]}.{record[37:39]}"),
            individual_identification_number=record[39:54].strip(),
            individual_name=record[54:76].strip(),
            discretionary_data=record[76:78].strip(),
            addenda_record_indicator=record[78],
            trace_number=record[79:94],
        )

    @staticmethod
    def parse_addenda_ppd(
            ach_records_type_7_id: UUID, record: str
    ) -> AchAddendaPpdSchema:
        return AchAddendaPpdSchema(
            ach_records_type_7_id=ach_records_type_7_id,
            record_type_code=record[0],
            addenda_type_code=record[1:3],
            payment_related_information=record[3:83].strip(),
            addenda_sequence_number=record[83:87],
            entry_detail_sequence_number=record[87:94],
        )

    @staticmethod
    def parse_batch_control(
            ach_records_type_8_id: UUID, record: str
    ) -> AchBatchControlSchema:
        return AchBatchControlSchema(
            ach_records_type_8_id=ach_records_type_8_id,
            record_type_code=record[0],
            service_class_code=record[1:4],
            entry_addenda_count=record[4:10],
            entry_hash=record[10:20].strip(),
            total_debit_entry_dollar_amount=Decimal(f"{record[20:30]}.{record[30:32]}"),
            total_credit_entry_dollar_amount=Decimal(
                f"{record[32:42]}.{record[42:44]}"
            ),
            company_identification=record[44:54].strip(),
            message_authentication_code=record[54:73].strip(),
            reserved=record[73:79].strip(),
            originating_dfi_identification=record[79:87],
            batch_number=record[87:94],
        )

    @staticmethod
    def parse_file_control(
            ach_records_type_9_id: UUID, record: str
    ) -> AchFileControlSchema:
        return AchFileControlSchema(
            ach_records_type_9_id=ach_records_type_9_id,
            record_type_code=record[0],
            batch_count=record[1:7],
            block_count=record[7:13],
            entry_addenda_count=record[13:21],
            entry_hash=record[21:31].strip(),
            total_debit_entry_dollar_amount=Decimal(f"{record[31:41]}.{record[41:43]}"),
            total_credit_entry_dollar_amount=Decimal(
                f"{record[43:53]}.{record[53:55]}"
            ),
            reserved=record[55:94],
        )

