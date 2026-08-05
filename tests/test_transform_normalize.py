from etl.transform.normalize import normalize_price_row


def test_normalize_price_row_converts_expected_fields():
    raw_row = {
        "good_name": "Milk",
        "good_price": "2980",
        "good_inspect_day": "2026-08-01",
        "entp_name": "Store A",
        "good_dc_yn": "Y",
    }
    normalized = normalize_price_row(raw_row)
    assert normalized.product_name == "Milk"
    assert normalized.price == 2980
    assert normalized.is_discounted is True
