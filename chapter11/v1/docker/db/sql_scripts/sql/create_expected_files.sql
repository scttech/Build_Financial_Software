-- Insert for Connect Comm
INSERT INTO company_expected_files ( company_id, file_name, schedule, last_file_date )
VALUES (
        (SELECT c.company_id FROM companies AS c WHERE tax_id_number = '136789452'),
        'connectcomm_daily_payments.ach',
        'daily',
        NOW() - INTERVAL '1 day'
       );

INSERT INTO company_expected_files ( company_id, file_name, schedule, last_file_date )
VALUES (
        (SELECT c.company_id FROM companies AS c WHERE tax_id_number = '136789452'),
        'connectcomm_daily_sweeps.ach',
        'daily',
        NOW() - INTERVAL '1 day'
       );

-- Insert for Elemental Resources
INSERT INTO company_expected_files ( company_id, file_name, schedule, last_file_date )
VALUES (
        (SELECT c.company_id FROM companies AS c WHERE tax_id_number = '459876543'),
        'elemental_resources_daily_billpay.ach',
        'daily',
        NOW() - INTERVAL '1 day'
       );

INSERT INTO company_expected_files ( company_id, file_name, schedule, last_file_date )
VALUES (
        (SELECT c.company_id FROM companies AS c WHERE tax_id_number = '459876543'),
        'elemental_resources.ach',
        'daily',
        NOW() - INTERVAL '1 day'
       );

-- Petro Power
INSERT INTO company_expected_files ( company_id, file_name, schedule, last_file_date )
VALUES (
        (SELECT c.company_id FROM companies AS c WHERE tax_id_number = '234567890'),
        'petro_power.ach',
        'daily',
        NOW() - INTERVAL '1 day'
       );


-- Insert for Stellar Services
INSERT INTO company_expected_files ( company_id, file_name, schedule, last_file_date )
VALUES (
        (SELECT c.company_id FROM companies AS c WHERE tax_id_number = '345678901'),
        'stellar_services.ach',
        'daily',
        NOW() - INTERVAL '1 day'
       );
