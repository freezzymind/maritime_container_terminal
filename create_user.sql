-- Creating user
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT FROM pg_catalog.pg_roles WHERE rolname = 'term_user'
    ) THEN
        EXECUTE format('CREATE USER term_user WITH ENCRYPTED PASSWORD %L;', :'term_user_password');
    END IF;
END $$;

GRANT CONNECT ON DATABASE sea_terminal TO term_user;
GRANT SELECT, UPDATE, INSERT ON ALL TABLES IN SCHEMA public TO term_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT, UPDATE, INSERT ON TABLES TO term_user;
REVOKE CREATE ON SCHEMA public FROM term_user;
