
-- Insert the ach_exception_codes
INSERT INTO ach_exception_codes (exception_code, exception_severity, exception_description) VALUES ('001', 'error', 'Record length is not 94 characters');
INSERT INTO ach_exception_codes (exception_code, exception_severity, exception_description) VALUES ('002', 'error', 'Record type was an unexpected value');
INSERT INTO ach_exception_codes (exception_code, exception_severity, exception_description) VALUES ('003', 'warning', 'Trace number out of order');
INSERT INTO ach_exception_codes (exception_code, exception_severity, exception_description) VALUES ('004', 'error', 'Invalid File ID Modifier');
INSERT INTO ach_exception_codes (exception_code, exception_severity, exception_description) VALUES ('005', 'error', 'Invalid Immediate Destination');

-- Insert the ach_recovery_options
INSERT INTO ach_recovery_options (exception_code, recovery_option) VALUES ('001', 'Request a corrected file from the originator');
INSERT INTO ach_recovery_options (exception_code, recovery_option) VALUES ('002', 'Request a corrected file from the originator');
INSERT INTO ach_recovery_options (exception_code, recovery_option) VALUES ('004', 'Specify a new File ID Modifier');

-- Insert the bank routing numbers
INSERT INTO bank_routing_numbers (routing_number, bank_name) VALUES ('990000013', 'Futuristic Fintech');
INSERT INTO bank_routing_numbers (routing_number, bank_name) VALUES ('990000026', 'Futuristic Fintech');
INSERT INTO bank_routing_numbers (routing_number, bank_name) VALUES ('990000039', 'Futuristic Fintech');
INSERT INTO bank_routing_numbers (routing_number, bank_name) VALUES ('991000009', 'Futuristic Fintech');
INSERT INTO bank_routing_numbers (routing_number, bank_name) VALUES ('991000012', 'Futuristic Fintech');
INSERT INTO bank_routing_numbers (routing_number, bank_name) VALUES ('992000024', 'Futuristic Fintech');
INSERT INTO bank_routing_numbers (routing_number, bank_name) VALUES ('992000037', 'Futuristic Fintech');
INSERT INTO bank_routing_numbers (routing_number, bank_name) VALUES ('993000049', 'Futuristic Fintech');
INSERT INTO bank_routing_numbers (routing_number, bank_name) VALUES ('993000052', 'Futuristic Fintech');