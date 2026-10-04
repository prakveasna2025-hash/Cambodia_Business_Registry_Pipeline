CREATE SCHEMA IF NOT EXISTS raw;

DROP TABLE IF EXISTS raw.raw_business_registry;

CREATE TABLE raw.raw_business_registry (
    id                       BIGSERIAL PRIMARY KEY,
    company_type             TEXT        NOT NULL,
    registration_count       TEXT,
    year                     TEXT        NOT NULL,
    loaded_at                TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_raw_business_registry_year ON raw.raw_business_registry (year);