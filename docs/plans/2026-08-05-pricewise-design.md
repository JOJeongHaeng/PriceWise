# PriceWise Project Design

**Date:** 2026-08-05
**Status:** Approved

## Goal

Build a standalone portfolio-ready data engineering project named `PriceWise` that collects Korean Consumer Agency consumer price data through the OpenAPI, stores and models it in PostgreSQL, and exposes analysis through a web dashboard.

## Scope

The first release includes:
- OpenAPI-based extraction of consumer price data
- PostgreSQL-based raw, core, and mart layers
- Batch ETL jobs for ingestion, cleaning, and aggregation
- Streamlit web dashboard for exploratory analysis and reporting
- GitHub-managed repository with documentation, tests, and CI

The first release excludes:
- Real-time streaming ingestion
- User accounts and authorization
- Production cloud deployment
- Advanced forecasting or ML pricing models

## Repository Structure

```text
PriceWise/
  app/
    dashboard/
    pages/
    components/
  etl/
    extract/
    transform/
    load/
    jobs/
  sql/
    schema/
    marts/
  tests/
  docs/
    plans/
  .env.example
  docker-compose.yml
  requirements.txt
  README.md
```

## Architecture

The project uses a single Python repository.

Data flow:
1. Call the Korean Consumer Agency OpenAPI
2. Persist raw responses and ingestion metadata
3. Normalize raw records into relational core tables
4. Build dashboard-facing aggregates in mart tables or views
5. Query marts from Streamlit for charts, tables, and KPIs

This design keeps source ingestion concerns separate from dashboard-facing analytics so that API changes, reruns, and deduplication can be handled in ETL without destabilizing the UI.

## Database Design

PostgreSQL is the primary database.

Schema layers:
- `raw`: API payloads, request metadata, ingestion timestamps, source keys
- `core`: normalized product, vendor, survey date, price, manufacturer, discount attributes
- `mart`: dashboard-focused aggregates such as price trends, lowest price comparisons, vendor comparisons, and discount summaries

Initial modeling principles:
- Preserve source traceability from mart rows back to raw records
- Separate dimensions from fact-like price observations where it improves query clarity
- Prefer idempotent loads keyed by source date and product/vendor identifiers
- Track ingestion and transform timestamps for rerun visibility

## ETL Design

The ETL is batch oriented and Python based.

Stages:
- `extract`: OpenAPI client, request pagination or batching, retry handling, response logging
- `transform`: XML parsing, column normalization, type conversion, deduplication, validation
- `load`: upsert or merge into PostgreSQL raw/core/mart layers
- `jobs`: entry points for full refresh and incremental refresh runs

Operational expectations:
- Config-driven API key and database connection management
- Structured logging for each ETL stage
- Fail-fast behavior for schema mismatches and malformed payloads
- Idempotent reruns for the same collection window where possible

## Dashboard Design

Streamlit is the primary dashboard framework.

Initial pages:
- `Overview`: total records, latest survey date, average price, discounted item count, coverage summary
- `Price Trends`: product-level time-series analysis by date range and product filters
- `Vendor Comparison`: compare the same product across vendors or retail channels
- `Discount Analysis`: compare discounted versus non-discounted prices and discount frequency

Initial dashboard requirements:
- Filter by product, vendor, and date range
- Load data from mart tables or views rather than raw/core tables
- Favor simple, readable charts and tabular drill-downs
- Support local demo execution with minimal setup

## Testing Strategy

Testing is required across ETL and dashboard query logic.

Test focus:
- API response parsing and normalization
- ETL transformation correctness for core fields
- Load idempotency and duplicate handling
- SQL mart correctness for key dashboard metrics
- Basic dashboard smoke tests for page rendering and query success

## GitHub Management

The project is managed as a standalone GitHub repository.

Repository workflow:
- `main` is the stable branch
- feature work is done in `feature/...` branches
- commits use conventional prefixes such as `feat:`, `fix:`, `docs:`, and `test:`
- GitHub Issues track major workstreams: ETL, schema, dashboard, docs, CI
- GitHub Actions runs tests on push or pull request

Documentation expectations:
- README includes project purpose, architecture, setup, and sample outputs
- docs/plans stores approved design and implementation planning artifacts
- data source attribution is shown clearly to satisfy license requirements

## Risks and Mitigations

- API schema or field changes
  - Mitigation: isolate parsing in extract/transform modules and validate required fields
- Duplicate or inconsistent source records
  - Mitigation: raw persistence plus deterministic normalization and load keys
- Dashboard performance degradation as data grows
  - Mitigation: query marts instead of normalized transactional tables
- Local environment friction
  - Mitigation: provide Docker Compose and `.env.example`

## Success Criteria

The first release is successful when:
- ETL can collect and store data from the OpenAPI into PostgreSQL
- dashboard marts support the required KPI, trend, vendor, and discount views
- Streamlit dashboard runs locally and displays usable analysis
- repository documentation is sufficient for another engineer to run the project
- the project is cleanly managed in GitHub with tests and CI
