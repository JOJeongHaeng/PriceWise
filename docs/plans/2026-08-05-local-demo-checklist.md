# PriceWise Local Demo Checklist

## Goal

Run the current PriceWise stack locally and verify the repository is ready for a basic demo.

## Steps

1. Start PostgreSQL with Docker Compose.

```bash
docker compose up -d db
```

2. Apply the schema SQL in this order.

```text
sql/schema/001_create_raw_schema.sql
sql/schema/002_create_core_schema.sql
sql/marts/001_price_trends.sql
sql/marts/002_vendor_comparison.sql
sql/marts/003_discount_summary.sql
```

3. Configure environment variables from `.env.example`.

4. Run the ETL entry logic after wiring the real API endpoint.

```bash
"/mnt/c/Users/goddl/AppData/Local/Programs/Python/Python311/python.exe" -c "from main import app_entrypoints; print(app_entrypoints()['pipeline'])"
```

5. Launch the Streamlit dashboard.

```bash
streamlit run app/dashboard/home.py
```

6. Verify the following pages exist in the UI.
- Overview
- Price Trends
- Vendor Comparison
- Discount Analysis

7. Confirm the repository test suite passes.

```bash
"/mnt/c/Users/goddl/AppData/Local/Programs/Python/Python311/python.exe" -m pytest -v
```
