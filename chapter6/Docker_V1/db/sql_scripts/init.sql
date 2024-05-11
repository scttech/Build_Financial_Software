SET search_path TO public;

-- Create the uuid extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create the ach_files table
CREATE TABLE ach_files (
    ach_files_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    file_name VARCHAR(255) NOT NULL,
    unparsed_record VARCHAR(94) NOT NULL,
    sequence_number INTEGER NOT NULL
);


