with staging as (

    select
        company_type,
        registration_year,
        registration_count
    from {{ ref('stg_business_registry') }}

),

aggregated as (

    select
        company_type,
        sum(registration_count)             as total_registrations,
        count(distinct registration_year)   as years_reported
    from staging
    group by company_type

)

select * from aggregated
order by total_registrations desc nulls last