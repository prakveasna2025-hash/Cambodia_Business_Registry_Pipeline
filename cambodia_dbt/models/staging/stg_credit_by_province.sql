with source as (

    select
        id,
        area,
        province,
        reporting_year,
        credit_balance_usd_m,
        credit_users_k,
        loaded_at
    from {{ source('raw', 'raw_credit_by_province') }}

),

renamed as (

    select
        id                              as credit_id,
        area,
        province,
        reporting_year,
        credit_balance_usd_m            as credit_balance_usd_millions,
        credit_users_k                  as credit_users_thousands,
        loaded_at
    from source

)

select * from renamed