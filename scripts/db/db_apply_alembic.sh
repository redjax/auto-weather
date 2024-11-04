#!/bin/bash

echo "Building Dockerfile for Alembic"
docker build -t auto-weather_alembic --target alembic -f ./Dockerfile .

echo "Applying latest Alembic migration"
docker run --rm \
    --name auto-weather-alembic_upgrade \
    --network auto-weathernet \
    -e DYNACONF_LOG_LEVEL=DEBUG \
    -e DYNACONF_DB_TYPE="${DB_TYPE:-postgres}" \
    -e DYNACONF_DB_DRIVERNAME="${DB_DRIVERNAME:-postgresql+psycopg2}" \
    -e DYNACONF_DB_HOST="${DB_HOST:-postgres}" \
    -e DYNACONF_DB_PORT="${DB_PORT:-5432}" \
    -e DYNACONF_DB_NAME="${DB_NAME:-auto_weather}" \
    -e DYNACONF_DB_USERNAME="${POSTGRES_USER:-postgres}" \
    -e DYNACONF_DB_PASSWORD="${POSTGRES_PASSWORD:-postgres}" \
    -e DYNACONF_DB_DATABASE="${POSTGRES_DATABASE:-auto_weather}" \
    -v ./src:/project/src \
    -v ./alembic.ini:/project/alembic.ini \
    -v ./migrations:/project/migrations \
    -v ./scripts:/project/scripts \
    -v ./noxfile.py:/project/noxfile.py \
    -w /project \
    -it \
    auto-weather_alembic \
    uv run nox -s alembic-upgrade
