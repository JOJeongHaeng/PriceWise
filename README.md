# PriceWise

PriceWise is a standalone data engineering and analytics project for collecting and analyzing Korean consumer price data from the Korean Consumer Agency OpenAPI.

## Stack

- Python
- PostgreSQL
- Streamlit
- SQLAlchemy

## Local Run

```bash
docker compose up -d db
```

Run tests:

```bash
"/mnt/c/Users/goddl/AppData/Local/Programs/Python/Python311/python.exe" -m pytest -v
```

Run dashboard:

```bash
streamlit run app/dashboard/home.py
```

## Data Source

- Korean Consumer Agency consumer price OpenAPI
