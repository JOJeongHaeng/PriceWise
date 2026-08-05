create schema if not exists mart;

create or replace view mart.vendor_comparison as
select
    product_name,
    vendor_name,
    survey_date,
    price,
    is_discounted
from core.price_observations;
