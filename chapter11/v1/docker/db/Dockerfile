FROM postgres:alpine

# Copy scripts to execute on container build
COPY sql_scripts/sql /docker-entrypoint-initdb.d/sql
COPY sql_scripts /docker-entrypoint-initdb.d/

# Healthcheck
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD pg_isready -U ${POSTGRES_USER} || exit 1

