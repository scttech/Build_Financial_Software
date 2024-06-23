-- Limits for Connect Comm
INSERT INTO company_limits ( company_id, daily_debit_limit, daily_credit_limit)
VALUES (
        (SELECT c.company_id FROM companies AS c WHERE tax_id_number = '136789452'),
        200.00,
        999999999.99
       );

-- Limits for Elemental Resources
INSERT INTO company_limits ( company_id, daily_debit_limit, daily_credit_limit)
VALUES (
        (SELECT c.company_id FROM companies AS c WHERE tax_id_number = '459876543'),
        400.00,
        750.00
       );

-- Limits for Stellar Services
INSERT INTO company_limits ( company_id, daily_debit_limit, daily_credit_limit)
VALUES (
        (SELECT c.company_id FROM companies AS c WHERE tax_id_number = '345678901'),
        200.00,
        1000.00
       );
