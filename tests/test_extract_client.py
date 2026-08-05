from etl.extract.client import PriceApiClient
from etl.extract.client import parse_price_rows


def test_client_builds_request_params():
    client = PriceApiClient(service_key="demo", page_no=1, num_of_rows=10)
    params = client.build_params()
    assert params["serviceKey"] == "demo"
    assert params["pageNo"] == 1
    assert params["numOfRows"] == 10


def test_parse_price_rows_extracts_items():
    xml_text = """<response><body><items><item><goodName>Milk</goodName></item></items></body></response>"""
    rows = parse_price_rows(xml_text)
    assert rows == [{"good_name": "Milk"}]
