ALTER TABLE raw.raw_business_registry
    DROP CONSTRAINT IF EXISTS uq_registry_type_year;

ALTER TABLE raw.raw_business_registry
    ADD CONSTRAINT uq_registry_type_year UNIQUE (company_type, year);