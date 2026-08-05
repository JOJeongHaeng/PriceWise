from pathlib import Path


def test_mart_sql_files_define_required_objects():
    trend_sql = Path("sql/marts/001_price_trends.sql").read_text(encoding="utf-8")
    vendor_sql = Path("sql/marts/002_vendor_comparison.sql").read_text(encoding="utf-8")
    discount_sql = Path("sql/marts/003_discount_summary.sql").read_text(encoding="utf-8")
    assert "mart.price_trends" in trend_sql
    assert "mart.vendor_comparison" in vendor_sql
    assert "mart.discount_summary" in discount_sql
