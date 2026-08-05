from etl.extract.client import parse_price_rows
from etl.transform.normalize import normalize_price_row


def run_pipeline(xml_text: str) -> list[dict[str, str | int | bool]]:
    rows = parse_price_rows(xml_text)
    normalized_rows = []
    for row in rows:
        normalized = normalize_price_row(row)
        normalized_rows.append(
            {
                "product_name": normalized.product_name,
                "price": normalized.price,
                "survey_date": normalized.survey_date,
                "vendor_name": normalized.vendor_name,
                "is_discounted": normalized.is_discounted,
            }
        )
    return normalized_rows
