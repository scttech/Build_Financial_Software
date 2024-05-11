SET search_path TO public;

-- Create the healthcheck table
CREATE TABLE health_check (
    id SERIAL PRIMARY KEY,
    status VARCHAR NOT NULL
);

-- Insert a row into the healthcheck table
INSERT INTO health_check (status) VALUES ('OK');

