from dataclasses import dataclass
import os


@dataclass
class Settings:
    pg_host: str
    pg_port: int
    pg_database: str
    pg_user: str
    pg_password: str
    consumer_api_key: str

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+psycopg://{self.pg_user}:{self.pg_password}"
            f"@{self.pg_host}:{self.pg_port}/{self.pg_database}"
        )

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            pg_host=os.getenv("PG_HOST", "localhost"),
            pg_port=int(os.getenv("PG_PORT", "5432")),
            pg_database=os.getenv("PG_DATABASE", "pricewise"),
            pg_user=os.getenv("PG_USER", "pricewise"),
            pg_password=os.getenv("PG_PASSWORD", "pricewise"),
            consumer_api_key=os.getenv("CONSUMER_API_KEY", ""),
        )
