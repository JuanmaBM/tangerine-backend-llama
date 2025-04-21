DO
$$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'postgres') THEN
        CREATE ROLE postgres LOGIN SUPERUSER PASSWORD 'postgres';
    END IF;
END
$$;

DO
$$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'citrus') THEN
        CREATE ROLE citrus LOGIN PASSWORD 'citrus' SUPERUSER;
    END IF;
END
$$;
