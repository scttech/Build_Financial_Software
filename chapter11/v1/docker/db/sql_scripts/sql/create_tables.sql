SET search_path TO public;

-- Create the uuid extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create the ach_files table
CREATE TABLE ach_files (
    ach_files_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    file_name VARCHAR(255) NOT NULL,
    file_hash VARCHAR(32) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Create the ach_records_type_1 table
CREATE TABLE ach_records_type_1 (
    ach_records_type_1_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    ach_files_id UUID NOT NULL REFERENCES ach_files(ach_files_id) ON DELETE CASCADE ON UPDATE CASCADE,
    unparsed_record VARCHAR(94) NOT NULL,
    sequence_number INTEGER NOT NULL
);

-- Create the ach_records_type_5 table
CREATE TABLE ach_records_type_5 (
    ach_records_type_5_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    ach_records_type_1_id UUID NOT NULL REFERENCES ach_records_type_1(ach_records_type_1_id) ON DELETE CASCADE ON UPDATE CASCADE,
    unparsed_record VARCHAR(94) NOT NULL,
    sequence_number INTEGER NOT NULL
);

-- Create the ach_records_type_6 table
CREATE TABLE ach_records_type_6 (
    ach_records_type_6_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    ach_records_type_5_id UUID NOT NULL REFERENCES ach_records_type_5(ach_records_type_5_id) ON DELETE CASCADE ON UPDATE CASCADE,
    unparsed_record VARCHAR(94) NOT NULL,
    sequence_number INTEGER NOT NULL
);

-- Create the ach_records_type_7 table
CREATE TABLE ach_records_type_7 (
    ach_records_type_7_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    ach_records_type_6_id UUID NOT NULL REFERENCES ach_records_type_6(ach_records_type_6_id) ON DELETE CASCADE ON UPDATE CASCADE,
    unparsed_record VARCHAR(94) NOT NULL,
    sequence_number INTEGER NOT NULL
);

-- Create the ach_records_type_8 table
CREATE TABLE ach_records_type_8 (
    ach_records_type_8_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    ach_records_type_5_id UUID NOT NULL REFERENCES ach_records_type_5(ach_records_type_5_id) ON DELETE CASCADE ON UPDATE CASCADE,
    unparsed_record VARCHAR(94) NOT NULL,
    sequence_number INTEGER NOT NULL
);

-- Create the ach_records_type_9 table
CREATE TABLE ach_records_type_9 (
    ach_records_type_9_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    ach_records_type_1_id UUID NOT NULL REFERENCES ach_records_type_1(ach_records_type_1_id) ON DELETE CASCADE ON UPDATE CASCADE,
    unparsed_record VARCHAR(94) NOT NULL,
    sequence_number INTEGER NOT NULL
);

-- Create the ach_records_type_invalid table
CREATE TABLE ach_records_type_invalid (
    ach_records_type_invalid_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    ach_files_id UUID NOT NULL REFERENCES ach_files(ach_files_id) ON DELETE CASCADE ON UPDATE CASCADE,
    unparsed_record VARCHAR(94) NOT NULL,
    sequence_number INTEGER NOT NULL
);

-- Create the ach_file_headers table
CREATE TABLE ach_file_headers (
    ach_records_type_1_id UUID NOT NULL REFERENCES ach_records_type_1(ach_records_type_1_id) ON DELETE CASCADE ON UPDATE CASCADE,
    record_type_code VARCHAR(1) NOT NULL,
    priority_code VARCHAR(2) NOT NULL,
    immediate_destination VARCHAR(10) NOT NULL,
    immediate_origin VARCHAR(10) NOT NULL,
    file_creation_date VARCHAR(6) NOT NULL,
    file_creation_time VARCHAR(4) NOT NULL,
    file_id_modifier VARCHAR(1) NOT NULL,
    record_size VARCHAR(3) NOT NULL,
    blocking_factor VARCHAR(2) NOT NULL,
    format_code VARCHAR(1) NOT NULL,
    immediate_destination_name VARCHAR(23) NOT NULL,
    immediate_origin_name VARCHAR(23) NOT NULL,
    reference_code VARCHAR(8) NOT NULL
);

-- Create the ach_batch_headers table
CREATE TABLE ach_batch_headers (
    ach_records_type_5_id UUID UNIQUE NOT NULL REFERENCES ach_records_type_5(ach_records_type_5_id) ON DELETE CASCADE ON UPDATE CASCADE,
    record_type_code VARCHAR(1) NOT NULL,
    service_class_code VARCHAR(3) NOT NULL,
    company_name VARCHAR(16) NOT NULL,
    company_discretionary_data VARCHAR(20) NOT NULL,
    company_identification VARCHAR(10) NOT NULL,
    standard_entry_class_code VARCHAR(3) NOT NULL,
    company_entry_description VARCHAR(10) NOT NULL,
    company_descriptive_date VARCHAR(6) NOT NULL,
    effective_entry_date VARCHAR(6) NOT NULL,
    settlement_date VARCHAR(3) NOT NULL,
    originator_status_code VARCHAR(1) NOT NULL,
    originating_dfi_identification VARCHAR(8) NOT NULL,
    batch_number VARCHAR(7) NOT NULL
);

-- Create the ach_entry_ppd_details table
CREATE TABLE ach_entry_ppd_details (
    ach_records_type_6_id UUID UNIQUE NOT NULL REFERENCES ach_records_type_6(ach_records_type_6_id) ON DELETE CASCADE ON UPDATE CASCADE,
    record_type_code VARCHAR(1) NOT NULL,
    transaction_code NUMERIC(2) NOT NULL,
    receiving_dfi_identification VARCHAR(8) NOT NULL,
    check_digit VARCHAR(1) NOT NULL,
    dfi_account_number VARCHAR(17) NOT NULL,
    amount NUMERIC(10,2) NOT NULL,
    individual_identification_number VARCHAR(15) NOT NULL,
    individual_name VARCHAR(22) NOT NULL,
    discretionary_data VARCHAR(2) NOT NULL,
    addenda_record_indicator VARCHAR(1) NOT NULL,
    trace_number VARCHAR(15) NOT NULL
);

-- Create the ach_addenda_ppd_records table
CREATE TABLE ach_addenda_ppd_records (
    ach_records_type_7_id UUID UNIQUE NOT NULL REFERENCES ach_records_type_7(ach_records_type_7_id) ON DELETE CASCADE ON UPDATE CASCADE,
    record_type_code VARCHAR(1) NOT NULL,
    addenda_type_code VARCHAR(2) NOT NULL,
    payment_related_information VARCHAR(80) NOT NULL,
    addenda_sequence_number VARCHAR(4) NOT NULL,
    entry_detail_sequence_number VARCHAR(7) NOT NULL
);

-- Create the ach_batch_control table
CREATE TABLE ach_batch_control_records (
    ach_records_type_8_id UUID UNIQUE NOT NULL REFERENCES ach_records_type_8(ach_records_type_8_id) ON DELETE CASCADE ON UPDATE CASCADE,
    record_type_code VARCHAR(1) NOT NULL,
    service_class_code NUMERIC(3) NOT NULL,
    entry_addenda_count NUMERIC(6) NOT NULL,
    entry_hash NUMERIC(10) NOT NULL,
    total_debit_entry_dollar_amount NUMERIC(12,2) NOT NULL,
    total_credit_entry_dollar_amount NUMERIC(12,2) NOT NULL,
    company_identification VARCHAR(10) NOT NULL,
    message_authentication_code VARCHAR(19) NOT NULL,
    reserved VARCHAR(6) NOT NULL,
    originating_dfi_identification VARCHAR(8) NOT NULL,
    batch_number NUMERIC(7) NOT NULL
);

-- Create the ach_file_control table
CREATE TABLE ach_file_control_records (
    ach_records_type_9_id UUID UNIQUE NOT NULL REFERENCES ach_records_type_9(ach_records_type_9_id) ON DELETE CASCADE ON UPDATE CASCADE,
    record_type_code VARCHAR(1) NOT NULL,
    batch_count VARCHAR(6) NOT NULL,
    block_count VARCHAR(6) NOT NULL,
    entry_addenda_count NUMERIC(8) NOT NULL,
    entry_hash VARCHAR(10) NOT NULL,
    total_debit_entry_dollar_amount NUMERIC(12, 2) NOT NULL,
    total_credit_entry_dollar_amount NUMERIC(12, 2) NOT NULL,
    reserved VARCHAR(39) NOT NULL
);

-- Create ENUM Type for ach_exception_severity
CREATE TYPE ach_exception_severity AS ENUM ('error', 'warning', 'info');

-- Create the ach_exception_codes
CREATE TABLE ach_exception_codes (
    ach_exception_codes_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    exception_code VARCHAR(3) NOT NULL UNIQUE,
    exception_severity ACH_EXCEPTION_SEVERITY NOT NULL,
    exception_description VARCHAR(255) NOT NULL
);

-- Create table for ach_recovery_options
CREATE TABLE ach_recovery_options (
    ach_recovery_options_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    exception_code VARCHAR(3) NOT NULL REFERENCES ach_exception_codes(exception_code) ON UPDATE CASCADE,
    recovery_option VARCHAR NOT NULL
);

-- Create the ach_exceptions table
CREATE TABLE ach_exceptions (
    ach_exceptions_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    ach_files_id UUID NOT NULL REFERENCES ach_files(ach_files_id) ON DELETE CASCADE ON UPDATE CASCADE,
    ach_records_type_5_id UUID REFERENCES ach_records_type_5(ach_records_type_5_id) ON DELETE CASCADE ON UPDATE CASCADE,
    ach_records_type_6_id UUID REFERENCES ach_records_type_6(ach_records_type_6_id) ON DELETE CASCADE ON UPDATE CASCADE,
    record_number NUMERIC NOT NULL,
    exception_code VARCHAR(3) NOT NULL REFERENCES ach_exception_codes(exception_code) ON UPDATE CASCADE
);

-- Create routing number table
CREATE TABLE bank_routing_numbers (
    routing_number VARCHAR(9) PRIMARY KEY,
    bank_name VARCHAR(255) NOT NULL
);

-- Create audit log table
CREATE TABLE audit_log (
    audit_log_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    user_id VARCHAR(25) DEFAULT NULL,
    ip_address INET DEFAULT NULL,
    user_agent VARCHAR(255) DEFAULT NULL,
    http_request VARCHAR(10) DEFAULT NULL,
    http_response NUMERIC(3) DEFAULT NULL,
    url VARCHAR(255) DEFAULT NULL,
    message TEXT NOT NULL
);

-- Create ENUM Type for industry_type
CREATE TYPE industry_type AS ENUM ('basic materials', 'consumer goods', 'consumer services', 'financials', 'healthcare', 'industrials', 'oil & gas', 'technology', 'telecommunications', 'utilities');

-- Create ENUM Type for tin_type
CREATE TYPE tin_type AS ENUM ('SSN', 'EIN', 'ITIN', 'ATIN', 'PTIN');

-- Company information table
CREATE TABLE companies (
    company_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    tax_id_type TIN_TYPE NOT NULL DEFAULT 'EIN',
    tax_id_number VARCHAR(9) NOT NULL,
    duns NUMERIC(9) NOT NULL,
    logo BYTEA DEFAULT NULL,
    website VARCHAR(255) DEFAULT NULL,
    industry INDUSTRY_TYPE DEFAULT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Create ENUM Type for address_type
CREATE TYPE address_type AS ENUM ('mailing', 'street');

-- Company address information
CREATE TABLE company_addresses (
    company_address_id UUID DEFAULT uuid_generate_v4(),
    company_id UUID NOT NULL REFERENCES companies(company_id) ON DELETE CASCADE ON UPDATE CASCADE,
    address_type ADDRESS_TYPE NOT NULL DEFAULT 'mailing',
    address_line_1 VARCHAR(255) NOT NULL,
    address_line_2 VARCHAR(255) DEFAULT NULL,
    address_line_3 VARCHAR(255) DEFAULT NULL,
    address_line_4 VARCHAR(255) DEFAULT NULL,
    city VARCHAR(255) NOT NULL,
    state VARCHAR(2) NOT NULL,
    zip_code NUMERIC(5) NOT NULL,
    zip_code_4 NUMERIC(4) DEFAULT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    PRIMARY KEY (company_id, address_type)
);

-- Create ENUM Type for phone_type
CREATE TYPE phone_type AS ENUM ( 'main', 'direct', 'department', 'fax', 'toll-free', 'mobile', 'home', 'other');

-- Company phone information
CREATE TABLE company_phones (
    company_phone_id UUID DEFAULT uuid_generate_v4(),
    company_id UUID NOT NULL REFERENCES companies(company_id) ON DELETE CASCADE ON UPDATE CASCADE,
    phone_type PHONE_TYPE NOT NULL DEFAULT 'main',
    phone_number NUMERIC(10) NOT NULL,
    extension NUMERIC(5) DEFAULT NULL,
    allow_sms BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    PRIMARY KEY (company_id, phone_type),
    UNIQUE (phone_number, extension)
);

-- Create a view
CREATE VIEW ach_combined_records AS
SELECT
    invalid.ach_records_type_invalid_id AS primary_key,
    invalid.unparsed_record,
    invalid.sequence_number,
    invalid.ach_files_id
FROM
    ach_records_type_invalid AS invalid

UNION ALL

SELECT
    r1.ach_records_type_1_id AS primary_key,
    r1.unparsed_record,
    r1.sequence_number,
    r1.ach_files_id
FROM
    ach_records_type_1 AS r1

UNION ALL

SELECT
    r5.ach_records_type_5_id,
    r5.unparsed_record,
    r5.sequence_number,
    r1_r5.ach_files_id
FROM
    ach_records_type_5 AS r5
JOIN ach_records_type_1 AS r1_r5 USING (ach_records_type_1_id)

UNION ALL

SELECT
    r6.ach_records_type_6_id,
    r6.unparsed_record,
    r6.sequence_number,
    r1_r6.ach_files_id
FROM
    ach_records_type_6 AS r6
JOIN ach_records_type_5 AS r5_r6 USING (ach_records_type_5_id)
JOIN ach_records_type_1 AS r1_r6 USING (ach_records_type_1_id)

UNION ALL

SELECT
    r7.ach_records_type_7_id,
    r7.unparsed_record,
    r7.sequence_number,
    r1_r7.ach_files_id
FROM
    ach_records_type_7 AS r7
JOIN ach_records_type_6 AS r6_r7 USING (ach_records_type_6_id)
JOIN ach_records_type_5 AS r5_r7 USING (ach_records_type_5_id)
JOIN ach_records_type_1 AS r1_r7 USING (ach_records_type_1_id)

UNION ALL

SELECT
    r8.ach_records_type_8_id,
    r8.unparsed_record,
    r8.sequence_number,
    r1_r8.ach_files_id
FROM
    ach_records_type_8 AS r8
JOIN ach_records_type_5 AS r5_r8 USING (ach_records_type_5_id)
JOIN ach_records_type_1 AS r1_r8 USING (ach_records_type_1_id)

UNION ALL

SELECT
    r9.ach_records_type_9_id,
    r9.unparsed_record,
    r9.sequence_number,
    r1_r9.ach_files_id
FROM
    ach_records_type_9 AS r9
JOIN ach_records_type_1 AS r1_r9 USING (ach_records_type_1_id);

-- Ensure changes are saved
COMMIT;
