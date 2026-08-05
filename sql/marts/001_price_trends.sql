create schema if not exists mart;

create or replace view mart.price_trends as
select
    product_name,
    survey_date,
    avg(price) as average_price,
    min(price) as lowest_price,
    max(price) as highest_price,
    count(*) as observation_count
from core.price_observations
group by product_name, survey_date;
