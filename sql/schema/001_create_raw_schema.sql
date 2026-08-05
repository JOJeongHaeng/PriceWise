create schema if not exists raw;

create table if not exists raw.price_api_responses (
    id bigserial primary key,
    collected_at timestamptz not null default now(),
    payload xml not null
);
