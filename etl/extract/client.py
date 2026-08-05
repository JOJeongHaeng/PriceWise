from dataclasses import dataclass

import requests
import xmltodict


@dataclass
class PriceApiClient:
    service_key: str
    page_no: int = 1
    num_of_rows: int = 100

    def build_params(self) -> dict[str, int | str]:
        return {
            "serviceKey": self.service_key,
            "pageNo": self.page_no,
            "numOfRows": self.num_of_rows,
        }

    def fetch(self, endpoint: str) -> str:
        response = requests.get(endpoint, params=self.build_params(), timeout=30)
        response.raise_for_status()
        return response.text


def parse_price_rows(xml_text: str) -> list[dict[str, str]]:
    parsed = xmltodict.parse(xml_text)
    items = parsed.get("response", {}).get("body", {}).get("items", {}).get("item", [])

    if isinstance(items, dict):
        items = [items]

    rows: list[dict[str, str]] = []
    for item in items:
        rows.append(
            {
                "good_name": item.get("goodName", ""),
            }
        )

    return rows
