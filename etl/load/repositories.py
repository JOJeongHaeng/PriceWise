def build_price_observation_key(product_name: str, vendor_name: str, survey_date: str) -> str:
    return f"{product_name}|{vendor_name}|{survey_date}"
