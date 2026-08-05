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
