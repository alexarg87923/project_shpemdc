FROM mysql:latest

# Copy the SQL template and init script
COPY ./init_mysql.sql.template /docker-entrypoint-initdb.d/init_mysql.sql.template
COPY ./init-db.sh /docker-entrypoint-initdb.d/init-db.sh

# Make init script executable
RUN chmod +x /docker-entrypoint-initdb.d/init-db.sh

EXPOSE 3306
