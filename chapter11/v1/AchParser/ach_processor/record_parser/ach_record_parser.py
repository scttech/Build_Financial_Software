import re
from decimal import Decimal
from uuid import UUID

from pydantic import ValidationError

from chapter11.v1.AchParser.ach_processor.record_parser.exceptions.ach_parsing_validation_error import (
    AchParsingValidationError,
)
from chapter11.v1.AchParser.ach_processor.schemas.database.ach.iat.ach_iat_710_addenda_schema import (
    AchIat710AddendaSchema,
)
from chapter11.v1.AchParser.ach_processor.schemas.database.ach.iat.ach_iat_711_addenda_schema import (
    AchIat711AddendaSchema,
)
from chapter11.v1.AchParser.ach_processor.schemas.database.ach.iat.ach_iat_712_addenda_schema import (
    AchIat712AddendaSchema,
)
from chapter11.v1.AchParser.ach_processor.schemas.database.ach.iat.ach_iat_713_addenda_schema import (
    AchIat713AddendaSchema,
)
from chapter11.v1.AchParser.ach_processor.schemas.database.ach.iat.ach_iat_714_addenda_schema import (
    AchIat714AddendaSchema,
)
from chapter11.v1.AchParser.ach_processor.schemas.database.ach.iat.ach_iat_715_addenda_schema import (
    AchIat715AddendaSchema,
)
from chapter11.v1.AchParser.ach_processor.schemas.database.ach.iat.ach_iat_716_addenda_schema import (
    AchIat716AddendaSchema,
)
from chapter11.v1.AchParser.ach_processor.schemas.database.ach.iat.ach_iat_batch_header_schema import (
    AchIatBatchHeaderSchema,
)
from chapter11.v1.AchParser.ach_processor.schemas.database.ach.iat.ach_iat_entry_details_schema import (
    AchIatEntryDetailsSchema,
)
from chapter11.v1.AchParser.ach_processor.schemas.database.ach_addenda_ppd_schema import (
    AchAddendaPpdSchema,
)
from chapter11.v1.AchParser.ach_processor.schemas.database.ach_batch_control_schema import (
    AchBatchControlSchema,
)
from chapter11.v1.AchParser.ach_processor.schemas.database.ach_batch_header_schema import (
    AchBatchHeaderSchema,
)
from chapter11.v1.AchParser.ach_processor.schemas.database.ach_entry_ppd_details_schema import (
    AchEntryPpdDetailsSchema,
)
from chapter11.v1.AchParser.ach_processor.schemas.database.ach_file_control_schema import (
    AchFileControlSchema,
)
from chapter11.v1.AchParser.ach_processor.schemas.database.ach_file_header_schema import (
    AchFileHeaderSchema,
)


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
            raise AchParsingValidationError(
                message="Error parsing file header", validation_errors=e.errors()
            )

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
    def parse_iat_batch_header(
        ach_records_type_5_id: UUID, record: str
    ) -> AchIatBatchHeaderSchema:
        return AchIatBatchHeaderSchema(
            ach_records_type_5_id=ach_records_type_5_id,
            record_type_code=record[0],
            service_class_code=record[1:4],
            iat_indicator=record[4:20].strip(),
            foreign_exchange_indicator=record[20:22],
            foreign_exchange_ref_indicator=record[22],
            foreign_exchange_reference=record[23:38].strip(),
            iso_destination_country_code=record[38:40],
            originator_id=record[40:50].strip(),
            standard_entry_class_code=record[50:53],
            company_entry_description=record[53:63].strip(),
            iso_originating_currency_code=record[63:66],
            iso_destination_currency_code=record[66:69],
            effective_entry_date=record[69:75],
            settlement_date=record[75:78],
            originator_status_code=record[78],
            originating_dfi_identification=record[79:87].strip(),
            batch_number=record[87:94].strip(),
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

    def parse_iat_entry_detail(
        self, ach_records_type_6_id, line
    ) -> AchIatEntryDetailsSchema:
        return AchIatEntryDetailsSchema(
            ach_records_type_6_id=ach_records_type_6_id,
            record_type_code=line[0],
            transaction_code=line[1:3],
            receiving_dfi_identification=line[3:11],
            number_of_addenda=line[12:17],
            amount=Decimal(f"{line[29:37]}.{line[37:38]}"),
            foreign_receivers_account_number=line[39:73].strip(),
            gateway_ofac_screening=line[76] == "1",
            secondary_ofac_screening=line[77] == "1",
            addenda_record_indicator=line[78],
            trace_number=line[79:94],
        )

    def parse_iat_addenda_710(
        self, ach_records_type_7_id, line
    ) -> AchIat710AddendaSchema:
        return AchIat710AddendaSchema(
            ach_records_type_7_id=ach_records_type_7_id,
            record_type_code=line[0],
            addenda_type_code=line[1:3],
            transaction_type_code=line[3:6],
            foreign_payment_amount=Decimal(f"{line[6:22]}.{line[22:24]}"),
            foreign_trace_number=line[24:46].strip(),
            receiving_name=line[46:81].strip(),
            entry_detail_sequence_number=line[87:94],
        )

    def parse_iat_addenda_711(
        self, ach_records_type_7_id, line
    ) -> AchIat711AddendaSchema:
        return AchIat711AddendaSchema(
            ach_records_type_7_id=ach_records_type_7_id,
            record_type_code=line[0],
            addenda_type_code=line[1:3],
            originator_name=line[3:38].strip(),
            originator_street_address=line[38:73].strip(),
            entry_detail_sequence_number=line[87:94],
        )

    def parse_iat_addenda_712(
        self, ach_records_type_7_id, line
    ) -> AchIat712AddendaSchema:
        regex = r"([^*]+)\*([^\\]+)\\"
        match = re.match(regex, line[3:38])
        if not match:
            raise ValueError("Error parsing originator city and state")
        originator_city, originator_state = match.groups()

        match = re.match(regex, line[38:73])
        if not match:
            raise ValueError("Error parsing originator country and postal code")
        originator_country, originator_postal_code = match.groups()

        return AchIat712AddendaSchema(
            ach_records_type_7_id=ach_records_type_7_id,
            record_type_code=line[0],
            addenda_type_code=line[1:3],
            originator_city=originator_city.strip(),
            originator_state=originator_state.strip(),
            originator_country=originator_country.strip(),
            originator_postal_code=originator_postal_code.strip(),
            entry_detail_sequence_number=line[87:94],
        )

    def parse_iat_addenda_713(
        self, ach_records_type_7_id, line
    ) -> AchIat713AddendaSchema:
        return AchIat713AddendaSchema(
            ach_records_type_7_id=ach_records_type_7_id,
            record_type_code=line[0],
            addenda_type_code=line[1:3],
            originating_dfi_name=line[3:38].strip(),
            originating_dfi_identification_qualifier=line[38:40].strip(),
            originating_dfi_identification=line[40:74].strip(),
            originating_dfi_branch_country_code=line[74:77].strip(),
            entry_detail_sequence_number=line[87:94],
        )

    def parse_iat_addenda_714(
        self, ach_records_type_7_id, line
    ) -> AchIat714AddendaSchema:
        return AchIat714AddendaSchema(
            ach_records_type_7_id=ach_records_type_7_id,
            record_type_code=line[0],
            addenda_type_code=line[1:3],
            receiving_dfi_name=line[3:38].strip(),
            receiving_dfi_identification_qualifier=line[38:40].strip(),
            receiving_dfi_identification=line[40:74].strip(),
            receiving_dfi_branch_country_code=line[74:77].strip(),
            entry_detail_sequence_number=line[87:94],
        )

    def parse_iat_addenda_715(
        self, ach_records_type_7_id, line
    ) -> AchIat715AddendaSchema:
        return AchIat715AddendaSchema(
            ach_records_type_7_id=ach_records_type_7_id,
            record_type_code=line[0],
            addenda_type_code=line[1:3],
            receiver_identification_number=line[3:18].strip(),
            receiver_street_address=line[18:53].strip(),
            entry_detail_sequence_number=line[87:94],
        )

    def parse_iat_addenda_716(
        self, ach_records_type_7_id, line
    ) -> AchIat716AddendaSchema:
        regex = r"([^*]+)\*([^\\]+)\\"
        match = re.match(regex, line[3:38])
        if not match:
            raise ValueError("Error parsing receiver city and state")
        receiver_city, receiver_state = match.groups()

        match = re.match(regex, line[38:73])
        if not match:
            raise ValueError("Error parsing receiver country and postal code")
        receiver_country, receiver_postal_code = match.groups()

        return AchIat716AddendaSchema(
            ach_records_type_7_id=ach_records_type_7_id,
            record_type_code=line[0],
            addenda_type_code=line[1:3],
            receiver_city=receiver_city.strip(),
            receiver_state=receiver_state.strip(),
            receiver_country=receiver_country.strip(),
            receiver_postal_code=receiver_postal_code.strip(),
            entry_detail_sequence_number=line[87:94],
        )
