from pathlib import Path


def test_streamlit_pages_exist():
    assert Path("app/dashboard/home.py").exists()
    assert Path("app/pages/1_price_trends.py").exists()
    assert Path("app/pages/2_vendor_comparison.py").exists()
    assert Path("app/pages/3_discount_analysis.py").exists()
