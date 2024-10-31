Our Docker files to setup a development environment for running PostgreSQL. 

This will setup the following:
Adminer
PostgreSQL
FastAPI

All tables have been refactored to ensure referential integrity, this version also goes with the V3 version of the APIs and parser.

This version refactors the ach_records table into its respective record types, creating new tables such as ach_records_type_1, ach_records_type_5, etc. This fixes the issue of having to use a generic table for all record types, which was causing issues with referential integrity where for instance when a batch is deleted not all records within the batch were deleted from the original ach_records table.

A view is built over the ach_records_type tables to allow for seeing the complete view that was previously available in ach_records.

This code goes with version (v4) of the ach_processor code and apis

Command to run to start the project:
```bash
docker-compose down; docker-compose up --build
```