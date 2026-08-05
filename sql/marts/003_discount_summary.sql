create schema if not exists mart;

create or replace view mart.discount_summary as
select
    survey_date,
    count(*) filter (where is_discounted) as discounted_count,
    count(*) filter (where not is_discounted) as regular_count,
    avg(price) filter (where is_discounted) as discounted_average_price,
    avg(price) filter (where not is_discounted) as regular_average_price
from core.price_observations
group by survey_date;
