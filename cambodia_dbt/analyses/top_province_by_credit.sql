select
    province,
    area,
    credit_balance_usd_millions,
    credit_users_thousands
from {{ ref('stg_credit_by_province') }}
order by credit_balance_usd_millions desc
limit 1