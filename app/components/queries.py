def build_overview_query() -> str:
    return """
    select
        count(*) as observation_count,
        max(survey_date) as latest_survey_date,
        avg(average_price) as average_price
    from mart.price_trends
    """
