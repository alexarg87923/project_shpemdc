#!/bin/bash
# This script runs during MySQL initialization
# MySQL already creates the database and user via MYSQL_DATABASE, MYSQL_USER, MYSQL_PASSWORD
# We just need to ensure the GRANT statement is executed

# Substitute environment variables in the SQL template using sed
# Write to /tmp first (writable location), then move to init directory
sed -e "s/\${MYSQL_DB_NAME}/${MYSQL_DB_NAME}/g" \
    -e "s/\${MYSQL_DB_USER}/${MYSQL_DB_USER}/g" \
    -e "s/\${MYSQL_DB_PASSWORD}/${MYSQL_DB_PASSWORD}/g" \
    /docker-entrypoint-initdb.d/init_mysql.sql.template > /tmp/01-init.sql

# Move the file to the init directory (ensure proper permissions)
mv /tmp/01-init.sql /docker-entrypoint-initdb.d/01-init.sql
chmod 644 /docker-entrypoint-initdb.d/01-init.sql

# Exit successfully - MySQL entrypoint will continue
exit 0

