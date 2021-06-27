#!/bin/sh
host=postgres
INIT_USER=${INIT_USER:-holis}
INIT_PASSWORD=${INIT_PASSWORD:-holis}
INIT_DB=${INIT_DB:-holis}

##https://github.com/cockroachdb/django-cockroachdb#faq
./cockroach sql --insecure -u root --host="$host" --execute="CREATE DATABASE IF NOT EXISTS ${INIT_DB};"

# Just in case
# ./cockroach sql --insecure -u root --host="$host" --execute="DROP DATABASE IF EXISTS ${INIT_DB} CASCADE; \
#                                         CREATE DATABASE IF NOT EXISTS ${INIT_DB}; \
#                                         CREATE USER IF NOT EXISTS ${INIT_USER}; \
#                                         GRANT ALL ON DATABASE ${INIT_DB} TO ${INIT_USER}; \
#                                         CREATE USER cockroach WITH PASSWORD '${INIT_PASSWORD}'";
