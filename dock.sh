# Пример генерации SQL-файла для создания пользователя
TEMP_SQL_FILE="/tmp/create_user.sql"
echo "CREATE USER term_user WITH ENCRYPTED PASSWORD '${TERM_USER_PASSWORD}';" > $TEMP_SQL_FILE
echo "GRANT CONNECT ON DATABASE sea_terminal TO term_user;" >> $TEMP_SQL_FILE
echo "GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA public TO term_user;" >> $TEMP_SQL_FILE

# Выполнение временного SQL-файла
PGPASSWORD="$POSTGRES_PASSWORD" psql -U postgres -d postgres -f $TEMP_SQL_FILE

# Удаление временного файла
rm -f $TEMP_SQL_FILE

# прописать дефолтный пароль в документацию
# указать где хранится созданный пароль (В КАКОМ ТОМЕ)


# Default password if running in detached mode or no input provided
DEFAULT_PASSWORD="default_example_password"

# Check if TERM_USER_PASSWORD is already set
if [[ -n "$TERM_USER_PASSWORD" ]]; then
  echo "TERM_USER_PASSWORD is already set. Using the provided password."
else
  # Check if running in interactive mode
  if [ -t 0 ]; then
    attempts=0
    max_attempts=3

    while [[ $attempts -lt $max_attempts ]]; do
      # Prompt for password
      read -sp "Create a password for term_user: " TERM_USER_PASSWORD
      echo
      # Check if password is empty
      if [[ -z "$TERM_USER_PASSWORD" ]]; then
        echo "Error: Password cannot be empty. Try again."
        attempts=$((attempts + 1))
        continue
      fi

      # Confirm password
      read -sp "Confirm the password: " TERM_USER_PASSWORD_CONFIRM
      echo
      # Check if passwords match
      if [[ "$TERM_USER_PASSWORD" != "$TERM_USER_PASSWORD_CONFIRM" ]]; then
        echo "Error: Passwords do not match. Try again."
        attempts=$((attempts + 1))
        continue
      fi

      # If both checks passed, break out of the loop
      break
    done

    # Fallback to default password after maximum attempts
    if [[ $attempts -ge $max_attempts ]]; then
      echo "Maximum attempts reached. Using default password."
      TERM_USER_PASSWORD="$DEFAULT_PASSWORD"
    fi
  else
    # Detached mode or non-interactive execution
    echo "Running in non-interactive mode. Using default password."
    TERM_USER_PASSWORD="$DEFAULT_PASSWORD"
  fi
fi

# Log the chosen password for debugging purposes (remove or restrict in production)
echo "Password for term_user: $TERM_USER_PASSWORD"
