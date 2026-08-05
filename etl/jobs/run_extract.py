from etl.extract.client import PriceApiClient
from etl.extract.client import parse_price_rows


def run_extract(endpoint: str, service_key: str) -> list[dict[str, str]]:
    client = PriceApiClient(service_key=service_key)
    xml_text = client.fetch(endpoint)
    return parse_price_rows(xml_text)
