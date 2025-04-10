#!/bin/bash
set -e

echo "Running envsubst on init_roles.sql.template..."
if [ -f /db_init/init_roles.sql.template ]; then
    envsubst < /db_init/init_roles.sql.template > /docker-entrypoint-initdb.d/init_roles.sql
    echo "Generated init_roles.sql"
fi

# Now execute the official entrypoint script
exec /usr/local/bin/docker-entrypoint.sh "$@"