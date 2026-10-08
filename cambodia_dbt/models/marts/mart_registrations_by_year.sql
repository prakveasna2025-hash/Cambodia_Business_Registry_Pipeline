with staging as (

    select
        registration_year,
        company_type,
        registration_count
    from {{ ref('stg_business_registry') }}

),

aggregated as (

    select
        registration_year,
        sum(registration_count)             as total_registrations,
        count(distinct company_type)        as distinct_company_types,
        count(*)                            as row_count
    from staging
    group by registration_year

)

select * from aggregated
order by registration_year