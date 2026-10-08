-- Custom test: fails if any registration_count is negative
select
    registry_id,
    registration_count
from {{ ref('stg_business_registry') }}
where registration_count < 0