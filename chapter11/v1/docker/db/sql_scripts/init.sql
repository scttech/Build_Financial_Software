SET search_path TO public;

-- Create tables
\i /docker-entrypoint-initdb.d/sql/create_tables.sql

-- Insert data
\i /docker-entrypoint-initdb.d/sql/general_ach_data.sql

-- Insert company information
\i /docker-entrypoint-initdb.d/sql/connect_comm_inc.sql
\i /docker-entrypoint-initdb.d/sql/elemental_resources_inc.sql
\i /docker-entrypoint-initdb.d/sql/innovatech_solutions.sql
\i /docker-entrypoint-initdb.d/sql/petro_power_llc.sql
\i /docker-entrypoint-initdb.d/sql/powergrid_utilities.sql
\i /docker-entrypoint-initdb.d/sql/quality_goods_co.sql
\i /docker-entrypoint-initdb.d/sql/secure_finance_group.sql
\i /docker-entrypoint-initdb.d/sql/stellar_services_ltd.sql
\i /docker-entrypoint-initdb.d/sql/titan_industries_corp.sql
\i /docker-entrypoint-initdb.d/sql/wellness_health_systems.sql

-- Ensure changes are saved
commit;

