with source as (

    select
        id,
        company_type,
        registration_count,
        year,
        loaded_at
    from {{ source('raw', 'raw_business_registry') }}

),

renamed as (

    select
        id                                          as registry_id,
        company_type,
        cast(registration_count as integer)         as registration_count,
        cast(year as integer)                       as registration_year,
        loaded_at
    from source

)

select * from renamed