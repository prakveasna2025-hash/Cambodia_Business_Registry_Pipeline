CREATE TABLE IF NOT EXISTS raw.raw_credit_by_province (
    id                    BIGSERIAL PRIMARY KEY,
    area                  TEXT        NOT NULL,
    province              TEXT        NOT NULL,
    reporting_year        INTEGER     NOT NULL,
    credit_balance_usd_m  NUMERIC(14,2) NOT NULL,
    credit_users_k        NUMERIC(10,2) NOT NULL,
    loaded_at             TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_credit_province_year UNIQUE (province, reporting_year)
);

CREATE INDEX IF NOT EXISTS idx_raw_credit_year ON raw.raw_credit_by_province (reporting_year);