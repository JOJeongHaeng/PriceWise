from dataclasses import dataclass


@dataclass
class NormalizedPriceRow:
    product_name: str
    price: int
    survey_date: str
    vendor_name: str
    is_discounted: bool


def normalize_price_row(raw_row: dict[str, str]) -> NormalizedPriceRow:
    return NormalizedPriceRow(
        product_name=raw_row["good_name"],
        price=int(raw_row["good_price"]),
        survey_date=raw_row["good_inspect_day"],
        vendor_name=raw_row["entp_name"],
        is_discounted=raw_row.get("good_dc_yn", "N") == "Y",
    )
