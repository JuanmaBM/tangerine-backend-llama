DO
$$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_database WHERE datname = 'llamastack') THEN
        CREATE DATABASE llamastack OWNER citrus;
    END IF;
END
$$;

DO
$$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_database WHERE datname = 'citrus') THEN
        CREATE DATABASE citrus OWNER citrus;
    END IF;
END
$$;

CREATE EXTENSION IF NOT EXISTS vector;
