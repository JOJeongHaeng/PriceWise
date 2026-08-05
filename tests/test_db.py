from db import build_engine


def test_build_engine_uses_database_url():
    engine = build_engine("postgresql+psycopg://user:pass@localhost:5432/db")
    assert "postgresql+psycopg" in str(engine.url)
