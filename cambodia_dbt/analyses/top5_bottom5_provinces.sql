-- Top 5 provinces by credit balance
select 'top_5' as bucket, province, area, credit_balance_usd_millions
from {{ ref('stg_credit_by_province') }}
order by credit_balance_usd_millions desc
limit 5

union all

-- Bottom 5 provinces by credit balance
select 'bottom_5' as bucket, province, area, credit_balance_usd_millions
from (
    select province, area, credit_balance_usd_millions
    from {{ ref('stg_credit_by_province') }}
    order by credit_balance_usd_millions asc
    limit 5
) bottom