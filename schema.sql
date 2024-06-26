DROP DATABASE IF EXISTS converter;
CREATE DATABASE converter;

\c converter
DROP TABLE IF EXISTS converter_users;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE converter_users (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    login VARCHAR(255) NOT NULL UNIQUE CHECK (login <> ''),
    password  VARCHAR(255) NOT NULL CHECK (length(password) >= 8)
);
