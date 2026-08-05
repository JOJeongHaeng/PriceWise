# PriceWise Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build the first working version of PriceWise with PostgreSQL-backed ETL, dashboard marts, and a local Streamlit web dashboard for consumer price analysis.

**Architecture:** PriceWise is a single Python repository with batch ETL and a Streamlit UI. Data flows from the Korean Consumer Agency OpenAPI into PostgreSQL `raw`, `core`, and `mart` schemas, and the dashboard reads only from mart-facing queries or views.

**Tech Stack:** Python 3.12, PostgreSQL, SQLAlchemy, psycopg, requests, xmltodict, pandas, Streamlit, pytest, Docker Compose, GitHub Actions

---

### Task 1: Bootstrap the repository

**Files:**
- Create: `README.md`
- Create: `.gitignore`
- Create: `.env.example`
- Create: `requirements.txt`
- Create: `docker-compose.yml`
- Create: `app/dashboard/__init__.py`
- Create: `app/pages/__init__.py`
- Create: `app/components/__init__.py`
- Create: `etl/extract/__init__.py`
- Create: `etl/transform/__init__.py`
- Create: `etl/load/__init__.py`
- Create: `etl/jobs/__init__.py`
- Create: `sql/schema/.gitkeep`
- Create: `sql/marts/.gitkeep`
- Create: `tests/__init__.py`
- Test: `tests/test_smoke.py`

**Step 1: Write the failing test**

```python
from pathlib import Path


def test_required_project_files_exist():
    required = [
        "README.md",
        ".env.example",
        "requirements.txt",
        "docker-compose.yml",
        "app/dashboard/__init__.py",
        "etl/extract/__init__.py",
        "tests/__init__.py",
    ]
    for path in required:
        assert Path(path).exists(), path
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_smoke.py -v`
Expected: FAIL with missing file assertions

**Step 3: Write minimal implementation**

Create the repository skeleton and minimal README, dependency list, local env example, and Docker Compose services for PostgreSQL and Streamlit.

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_smoke.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add README.md .gitignore .env.example requirements.txt docker-compose.yml app etl sql tests
git commit -m "feat: bootstrap PriceWise project structure"
```

### Task 2: Add configuration and database connectivity

**Files:**
- Create: `config.py`
- Create: `db.py`
- Create: `tests/test_config.py`
- Create: `tests/test_db.py`
- Modify: `requirements.txt`
- Modify: `.env.example`

**Step 1: Write the failing test**

```python
from config import Settings


def test_settings_build_database_url():
    settings = Settings(
        pg_host="localhost",
        pg_port=5432,
        pg_database="pricewise",
        pg_user="pricewise",
        pg_password="secret",
        consumer_api_key="demo",
    )
    assert settings.database_url == "postgresql+psycopg://pricewise:secret@localhost:5432/pricewise"
```

```python
from db import build_engine


def test_build_engine_uses_database_url():
    engine = build_engine("postgresql+psycopg://user:pass@localhost:5432/db")
    assert "postgresql+psycopg" in str(engine.url)
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_config.py tests/test_db.py -v`
Expected: FAIL with import errors for `config` and `db`

**Step 3: Write minimal implementation**

Implement a small settings object that reads environment values and exposes a computed `database_url`. Add SQLAlchemy engine/session helpers in `db.py`.

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_config.py tests/test_db.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add config.py db.py .env.example requirements.txt tests/test_config.py tests/test_db.py
git commit -m "feat: add configuration and database helpers"
```

### Task 3: Implement raw extraction from the OpenAPI

**Files:**
- Create: `etl/extract/client.py`
- Create: `etl/extract/models.py`
- Create: `etl/jobs/run_extract.py`
- Create: `tests/test_extract_client.py`
- Modify: `requirements.txt`

**Step 1: Write the failing test**

```python
from etl.extract.client import PriceApiClient


def test_client_builds_request_params():
    client = PriceApiClient(service_key="demo", page_no=1, num_of_rows=10)
    params = client.build_params()
    assert params["serviceKey"] == "demo"
    assert params["pageNo"] == 1
    assert params["numOfRows"] == 10
```

```python
from etl.extract.client import parse_price_rows


def test_parse_price_rows_extracts_items():
    xml_text = \"\"\"<response><body><items><item><goodName>Milk</goodName></item></items></body></response>\"\"\"
    rows = parse_price_rows(xml_text)
    assert rows == [{"good_name": "Milk"}]
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_extract_client.py -v`
Expected: FAIL with missing module or function errors

**Step 3: Write minimal implementation**

Build a requests-based client with parameter generation, HTTP fetch logic, XML parsing, and normalized raw row mapping. Keep the first version limited to fields required by the design.

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_extract_client.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add etl/extract/client.py etl/extract/models.py etl/jobs/run_extract.py tests/test_extract_client.py requirements.txt
git commit -m "feat: add OpenAPI extraction client"
```

### Task 4: Implement transformation logic and core data model loading

**Files:**
- Create: `etl/transform/normalize.py`
- Create: `etl/load/repositories.py`
- Create: `etl/jobs/run_pipeline.py`
- Create: `sql/schema/001_create_raw_schema.sql`
- Create: `sql/schema/002_create_core_schema.sql`
- Create: `tests/test_transform_normalize.py`
- Create: `tests/test_load_repositories.py`

**Step 1: Write the failing test**

```python
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
```

```python
from etl.load.repositories import build_price_observation_key


def test_build_price_observation_key_is_deterministic():
    key = build_price_observation_key(
        product_name="Milk",
        vendor_name="Store A",
        survey_date="2026-08-01",
    )
    assert key == "Milk|Store A|2026-08-01"
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_transform_normalize.py tests/test_load_repositories.py -v`
Expected: FAIL with import errors

**Step 3: Write minimal implementation**

Add normalized dataclasses or typed models, field casting, validation of required fields, and simple repository helpers for idempotent raw/core persistence keys.

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_transform_normalize.py tests/test_load_repositories.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add etl/transform/normalize.py etl/load/repositories.py etl/jobs/run_pipeline.py sql/schema/001_create_raw_schema.sql sql/schema/002_create_core_schema.sql tests/test_transform_normalize.py tests/test_load_repositories.py
git commit -m "feat: add normalization and core load logic"
```

### Task 5: Add mart SQL for dashboard analytics

**Files:**
- Create: `sql/marts/001_price_trends.sql`
- Create: `sql/marts/002_vendor_comparison.sql`
- Create: `sql/marts/003_discount_summary.sql`
- Create: `tests/test_mart_sql.py`

**Step 1: Write the failing test**

```python
from pathlib import Path


def test_mart_sql_files_define_required_objects():
    trend_sql = Path("sql/marts/001_price_trends.sql").read_text(encoding="utf-8")
    vendor_sql = Path("sql/marts/002_vendor_comparison.sql").read_text(encoding="utf-8")
    discount_sql = Path("sql/marts/003_discount_summary.sql").read_text(encoding="utf-8")
    assert "mart.price_trends" in trend_sql
    assert "mart.vendor_comparison" in vendor_sql
    assert "mart.discount_summary" in discount_sql
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_mart_sql.py -v`
Expected: FAIL with missing file errors

**Step 3: Write minimal implementation**

Create SQL views or materialized views for trend, vendor comparison, and discount summary queries using only core tables and clear column names for the dashboard.

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_mart_sql.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add sql/marts/001_price_trends.sql sql/marts/002_vendor_comparison.sql sql/marts/003_discount_summary.sql tests/test_mart_sql.py
git commit -m "feat: add mart SQL for dashboard analytics"
```

### Task 6: Build Streamlit dashboard pages

**Files:**
- Create: `app/dashboard/home.py`
- Create: `app/pages/1_price_trends.py`
- Create: `app/pages/2_vendor_comparison.py`
- Create: `app/pages/3_discount_analysis.py`
- Create: `app/components/queries.py`
- Create: `tests/test_dashboard_queries.py`
- Create: `tests/test_dashboard_smoke.py`

**Step 1: Write the failing test**

```python
from app.components.queries import build_overview_query


def test_build_overview_query_targets_mart_tables():
    query = build_overview_query()
    assert "mart." in query
    assert "raw." not in query
```

```python
from pathlib import Path


def test_streamlit_pages_exist():
    assert Path("app/dashboard/home.py").exists()
    assert Path("app/pages/1_price_trends.py").exists()
    assert Path("app/pages/2_vendor_comparison.py").exists()
    assert Path("app/pages/3_discount_analysis.py").exists()
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_dashboard_queries.py tests/test_dashboard_smoke.py -v`
Expected: FAIL with missing file or import errors

**Step 3: Write minimal implementation**

Add a Streamlit home page with KPI cards and separate pages for trends, vendor comparison, and discount analysis. Centralize SQL query strings in `app/components/queries.py`.

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_dashboard_queries.py tests/test_dashboard_smoke.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add app/dashboard/home.py app/pages app/components/queries.py tests/test_dashboard_queries.py tests/test_dashboard_smoke.py
git commit -m "feat: add Streamlit dashboard pages"
```

### Task 7: Add local run scripts, CI, and documentation polish

**Files:**
- Create: `main.py`
- Create: `.github/workflows/test.yml`
- Modify: `README.md`
- Create: `tests/test_main.py`

**Step 1: Write the failing test**

```python
from main import app_entrypoints


def test_app_entrypoints_exposes_pipeline_and_dashboard():
    entrypoints = app_entrypoints()
    assert "pipeline" in entrypoints
    assert "dashboard" in entrypoints
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_main.py -v`
Expected: FAIL with import error for `main`

**Step 3: Write minimal implementation**

Create a simple project entry module that documents how to run pipeline and dashboard commands, add a GitHub Actions workflow that installs dependencies and runs pytest, and update README with setup, architecture, and attribution.

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_main.py -v`
Expected: PASS

**Step 5: Run the full verification suite**

Run: `pytest -v`
Expected: PASS for all tests

**Step 6: Commit**

```bash
git add main.py .github/workflows/test.yml README.md tests/test_main.py
git commit -m "feat: add entrypoints, CI, and project docs"
```

### Task 8: Verify local stack and capture demo readiness

**Files:**
- Modify: `README.md`
- Create: `docs/plans/2026-08-05-local-demo-checklist.md`

**Step 1: Write the failing test**

```python
from pathlib import Path


def test_demo_checklist_exists():
    assert Path("docs/plans/2026-08-05-local-demo-checklist.md").exists()
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_smoke.py::test_required_project_files_exist tests/test_main.py::test_app_entrypoints_exposes_pipeline_and_dashboard -v`
Expected: FAIL because the checklist file does not exist

**Step 3: Write minimal implementation**

Document the local demo flow: bring up PostgreSQL, run schema SQL, run ETL job, launch Streamlit, and validate the four dashboard pages with sample filters.

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_smoke.py::test_required_project_files_exist tests/test_main.py::test_app_entrypoints_exposes_pipeline_and_dashboard -v`
Expected: PASS

**Step 5: Commit**

```bash
git add README.md docs/plans/2026-08-05-local-demo-checklist.md
git commit -m "docs: add local demo checklist"
```
