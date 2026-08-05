create schema if not exists core;

create table if not exists core.price_observations (
    observation_key text primary key,
    product_name text not null,
    vendor_name text not null,
    survey_date date not null,
    price integer not null,
    is_discounted boolean not null default false
);
