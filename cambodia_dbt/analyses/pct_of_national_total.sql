with national as (

    select
        sum(credit_balance_usd_millions) as national_total
    from {{ ref('stg_credit_by_province') }}

),

per_province as (

    select
        province,
        area,
        credit_balance_usd_millions
    from {{ ref('stg_credit_by_province') }}

)

select
    p.province,
    p.area,
    p.credit_balance_usd_millions,
    round(
        p.credit_balance_usd_millions * 100.0 / n.national_total,
        2
    ) as pct_of_national
from per_province p
cross join national n
order by pct_of_national desc