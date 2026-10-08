with staging as (

    select
        area,
        province,
        credit_balance_usd_millions,
        credit_users_thousands
    from {{ ref('stg_credit_by_province') }}

),

aggregated as (

    select
        area,
        sum(credit_balance_usd_millions)    as total_credit_usd_millions,
        sum(credit_users_thousands)         as total_users_thousands,
        count(*)                            as province_count
    from staging
    group by area

)

select * from aggregated
order by total_credit_usd_millions desc