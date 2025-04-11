# ./db/Dockerfile
FROM postgres:15-alpine

# Install envsubst (from gettext)
RUN apk add --no-cache gettext

# Place both the template and our custom entrypoint script into /docker-entrypoint-initdb.d
COPY /db_init/ /db_init/

# Make the script executable
RUN chmod +x /db_init/entrypoint.sh

# Use our custom entrypoint script (it will call the original afterwards)
ENTRYPOINT ["/db_init/docker-entrypoint-init.sh"]

CMD ["postgres"]
