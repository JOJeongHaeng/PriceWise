from etl.load.repositories import build_price_observation_key


def test_build_price_observation_key_is_deterministic():
    key = build_price_observation_key(
        product_name="Milk",
        vendor_name="Store A",
        survey_date="2026-08-01",
    )
    assert key == "Milk|Store A|2026-08-01"
