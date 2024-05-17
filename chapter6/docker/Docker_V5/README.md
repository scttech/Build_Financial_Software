Our Docker files to setup a development environment for running PostgreSQL. 

This will setup the following:
Adminer
PostgreSQL
FastAPI

This contains the working project with updated SQL changes to support uploading a file and storing it in the database while ensuring referential integrity with the use of foriegn keys.

Command to run to start the project:
```bash
docker-compose down; docker-compose up --build
```