#!/bin/bash


## Database name
DB_NAME="${DB_NAME:-auto_weather}"
## Database user
DB_USER="${DB_USER:-postgres}"
## Database password
DB_PASSWORD="${DB_PASSWORD:-postgres}"
## Host of the database (could be a container name or IP)
DB_HOST="${DB_HOST:-localhost}"
## Port of the database
DB_PORT="${DB_PORT:-5432}"
## Local backup directory
BACKUP_DIR="${BACKUP_DIR:-./backups/db}"
## Container version for postgres
PG_IMG_VER="${PG_IMG_VER:-bullseye}"

# Timestamp for backup file naming
TIMESTAMP=$(date +"%Y%m%d%H%M%S")
BACKUP_FILE="${BACKUP_DIR}/${DB_NAME}_backup_${TIMESTAMP}.sql"

# Ensure the backup directory exists
mkdir -pv "$BACKUP_DIR"

# Run a temporary PostgreSQL client container to create the backup
docker run --rm \
    --network="host" \
    -e PGPASSWORD="${DB_PASSWORD}" \
    -v "${BACKUP_DIR}:/backup" \
    postgres:$PG_IMG_VER \
    pg_dump -h "${DB_HOST}" -p "${DB_PORT}" -U "${DB_USER}" -F c -b -f "/backup/${DB_NAME}_backup_${TIMESTAMP}.sql" "${DB_NAME}"

# Check if the backup was created
if [[ -f "${BACKUP_FILE}" ]]; then
    echo "Backup successful: ${BACKUP_FILE}"
else
    echo "Backup failed."
fi
