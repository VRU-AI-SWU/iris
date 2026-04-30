from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    model_config = ConfigDict(env_file=".env", protected_namespaces=())

    model_server_url: str = "http://host.docker.internal:1234/v1"
    model_api_key: str = "lm-studio"
    extraction_model: str = "gemma-4-31b-it"
    embedding_model: str = "text-embedding-embeddinggemma-300m"

    database_url: str = "postgresql://iris:iris_dev_password@postgres:5432/iris"
    redis_url: str = "redis://redis:6379/0"

    secret_key: str = "change-me"
    debug: bool = False
    log_level: str = "INFO"

    scrape_delay: float = 2.0
    scrape_concurrency: int = 2
    job_posting_window_months: int = 12


settings = Settings()
