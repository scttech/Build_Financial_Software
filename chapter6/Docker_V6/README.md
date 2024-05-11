Our Docker files to setup a development environment for running PostgreSQL. 

This will setup the following:
Adminer
PostgreSQL
FastAPI

All tables have been refactored to ensure referential integrity, this version also goes with the V3 version of the APIs and parser

Command to run to start the project:
```bash
docker-compose down; docker-compose up --build
```