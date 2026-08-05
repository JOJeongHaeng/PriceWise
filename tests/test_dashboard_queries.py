from app.components.queries import build_overview_query


def test_build_overview_query_targets_mart_tables():
    query = build_overview_query()
    assert "mart." in query
    assert "raw." not in query
