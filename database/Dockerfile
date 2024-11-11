# Use the official PostgreSQL image
FROM postgres:latest

ENV POSTGRES_DB=filesystem_db
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=mysecretpassword

COPY ./init.sql /docker-entrypoint-initdb.d/
RUN chmod +x /docker-entrypoint-initdb.d/*.sql
# Environment variables are set in docker-compose.yml