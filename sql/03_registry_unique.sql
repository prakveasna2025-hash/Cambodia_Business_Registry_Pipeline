ALTER TABLE raw.raw_business_registry
    ADD CONSTRAINT uq_registry_type_year UNIQUE (company_type, year);