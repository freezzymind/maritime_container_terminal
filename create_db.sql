-- Creating database
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT FROM pg_database WHERE datname = :new_db_name
    ) THEN
        EXECUTE format('CREATE DATABASE %I OWNER postgres', :new_db_name);
    END IF;
END $$;

