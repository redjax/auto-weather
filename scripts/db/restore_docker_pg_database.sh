#!/bin/bash

# Database name
DB_NAME="${DB_NAME:-auto_weather}"
# Database user
DB_USER="${DB_USER:-postgres}"
# Database password
DB_PASSWORD="${DB_PASSWORD:-postgres}"
# Host of the database (could be a container name or IP)
DB_HOST="${DB_HOST:-localhost}"
# Port of the database
DB_PORT="${DB_PORT:-5432}"
# Container version for postgres
PG_IMG_VER="${PG_IMG_VER:-bullseye}"

# Prompt the user for the backup file path
read -p "Enter the path to the backup file (e.g., ./backups/auto_weather_backup_20241104052821.sql): " BACKUP_FILE

# Check if the specified backup file exists
if [[ ! -f "$BACKUP_FILE" ]]; then
    echo "Backup file not found: $BACKUP_FILE"
    exit 1
fi

# Get the directory of the backup file
BACKUP_DIR="$(dirname "$BACKUP_FILE")"
BACKUP_FILENAME="$(basename "$BACKUP_FILE")"

# Run a temporary PostgreSQL client container to restore the backup
docker run --rm \
    --network="host" \
    -e PGPASSWORD="${DB_PASSWORD}" \
    -v "${BACKUP_DIR}:/backup" \
    postgres:$PG_IMG_VER \
    pg_restore -h "${DB_HOST}" -p "${DB_PORT}" -U "${DB_USER}" -d "${DB_NAME}" "/backup/${BACKUP_FILENAME}"

# Check if the restore was successful
if [[ $? -eq 0 ]]; then
    echo "Restore successful: ${BACKUP_FILE} to database ${DB_NAME}"
else
    echo "Restore failed."
fi
