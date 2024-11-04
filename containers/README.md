# Container Data

For local development, you can create host mounts to persists data. To do this, edit the [`.env`](../.env.example) file and for any variable that mounts a volume/path, set a path in [`./containers/vols`](./vols/).

Example: Mount the redis container's data directory to `./containers/vols/redis/data`:

```text
## .env

...

## Default: (named volume) redis_data
REDIS_DATA_DIR=./containers/vols/redis/data

...

```

```yaml
## docker-compose.yml
---

...


services:
    ...

    redis:
        image: ...
        container_name: ...
        volumes:
            - ${REDIS_DATA_DIR:-redis_data}:/data

...

```

The above configuration would create a path `./containers/vols/redis/data`, and mount the Redis container's `/data` path to this directory.

## Note on mounting postgres data directory

If you mount the `postgres` container's `/var/lib/postgresql/data` path to a host volume/local directory, note that the directory will appear empty if you don't have permissions to view it. This is ok! **Don't change the owner of your host volume mount**, it'll break the database.

You can view the contents of that directory with `sudo ls ./containers/vols/postgres/data`.

## Postgres init script

The [`pg_entrypoint.sh`](./vols/postgres/pg_entrypoint/pg_entrypoint.sh) script is mounted in the `postgres` container and executed when the database is created. This script installs plugins & does any default setup steps you describe.

```shell
#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USERNAME" --dbname="$POSTGRES_DATABASE" <<-EOSQL
   CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
EOSQL
```
