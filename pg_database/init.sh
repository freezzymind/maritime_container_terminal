#!/bin/bash

# 1. Creating database
TEMP_SQL_DB="/tmp/create_db.sql"
echo "CREATE DATABASE sea_terminal;" > "$TEMP_SQL_DB"

PGPASSWORD="$POSTGRES_PASSWORD" psql -U postgres -d postgres -f "$TEMP_SQL_DB"
rm -f "$TEMP_SQL_DB"
echo "Database 'sea_terminal' created successfully."


# 2. Creating tables
TEMP_SQL_TABLES="/tmp/create_tables.sql"
cat <<EOT > "$TEMP_SQL_TABLES"
CREATE TABLE ships (
id SERIAL PRIMARY KEY,
name VARCHAR(100) NOT NULL,
imo CHAR(7) NOT NULL UNIQUE CHECK (imo ~ '^\d{7}$'),
flag VARCHAR(50) NOT NULL,
gross_tonnage INTEGER NOT NULL CHECK (gross_tonnage > 1000 AND gross_tonnage < 999999),
length NUMERIC(10, 2) NOT NULL,
width NUMERIC(10, 2) NOT NULL,
draft NUMERIC(10, 2) NOT NULL,
location VARCHAR(100));

CREATE UNIQUE INDEX idx_ships_imo ON ships(imo);
CREATE INDEX idx_ships_location ON ships(location); 


CREATE TABLE berths (
id SERIAL PRIMARY KEY,
status VARCHAR(10) NOT NULL CHECK (status IN ('free', 'busy', 'reserved')),
max_draft NUMERIC(10, 2) NOT NULL,
max_length NUMERIC(10, 2) NOT NULL,
ship_name VARCHAR(100),
ship_imo CHAR(7) REFERENCES ships(imo) CHECK (ship_imo ~ '^\d{7}$'));

CREATE INDEX idx_berths_ship_imo ON berths(ship_imo);
CREATE INDEX idx_berths_conditions ON berths(status, max_draft, max_length); 


CREATE TABLE port_calls (
id SERIAL PRIMARY KEY,
imo CHAR(7) NOT NULL REFERENCES ships(imo) CHECK (imo ~ '^\d{7}$'),
arrival_time TIMESTAMP NOT NULL);


CREATE TABLE port_departs (
id SERIAL PRIMARY KEY,
imo CHAR(7) NOT NULL REFERENCES ships(imo) CHECK (imo ~ '^\d{7}$'),
departure_time TIMESTAMP NOT NULL);
EOT

PGPASSWORD="$POSTGRES_PASSWORD" psql -U postgres -d sea_terminal -f "$TEMP_SQL_TABLES"
rm -f "$TEMP_SQL_TABLES"
echo "All tables created successfully."


# 3. Creating password for term_user
# Check if an environment variable with the password was provided
if [[ -n "$TERM_USER_PASSWORD" ]]; then
  echo "TERM_USER_PASSWORD was provided. Skipping password prompt."
else
  # Check if running in detached mode (background)
  if [[ ! -t 0 ]]; then
    echo "Running in detached mode. Using default password - 'not_secure'."
    TERM_USER_PASSWORD="not_secure"
  else
    # Maximum number of password input attempts
    attempts=0
    max_attempts=3

    while [[ $attempts -lt $max_attempts ]]; do
      # Prompt the user for a password
      read -sp "Create a password for term_user: " TERM_USER_PASSWORD
      echo
      if [[ -z "$TERM_USER_PASSWORD" ]]; then
        echo "Error: Password cannot be empty. Try again."
        attempts=$((attempts + 1))
        continue
      fi

      # Confirm the password
      read -sp "Confirm the password: " TERM_USER_PASSWORD_CONFIRM
      echo
      if [[ "$TERM_USER_PASSWORD" != "$TERM_USER_PASSWORD_CONFIRM" ]]; then
        echo "Error: Passwords do not match. Try again."
        attempts=$((attempts + 1))
        continue
      fi

      break
    done

    # If the attempt limit is exceeded, use the default password
    if [[ $attempts -ge $max_attempts ]]; then
      echo "Maximum attempts reached. Using default password - 'not_secure'."
      TERM_USER_PASSWORD="not_secure"
    fi
  fi
fi


# 4. Creating user
TEMP_SQL_USER="/tmp/create_user.sql"
cat <<EOT > "$TEMP_SQL_USER"
CREATE USER term_user WITH ENCRYPTED PASSWORD '${TERM_USER_PASSWORD}';
GRANT CONNECT ON DATABASE sea_terminal TO term_user;
GRANT USAGE ON SCHEMA public TO term_user;
GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA public TO term_user;
EOT

PGPASSWORD="$POSTGRES_PASSWORD" psql -U postgres -d sea_terminal -f "$TEMP_SQL_USER"
rm -f "$TEMP_SQL_USER"
echo "User 'term_user' created successfully."


# 5. Save the password in a /secure directory inside PostgreSQL data volume
mkdir -p /var/lib/postgresql/data/secure
SECURE_PATH="/var/lib/postgresql/data/secure/term_user_password.txt"
echo "$TERM_USER_PASSWORD" > "$SECURE_PATH"
chmod 644 "$SECURE_PATH"
echo "Password for term_user saved in $SECURE_PATH."
