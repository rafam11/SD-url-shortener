from src.core import constants as cons

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=cons.ENV_FILE_FORMAT, env_file_encoding=cons.UTF8_ENCODING
    )
    postgres_db: str | None = None
    postgres_user: str | None = None
    postgres_password: str | None = None
    postgres_host: str | None = None
    postgres_port: int | None = None

    @property
    def postgres_url(self) -> PostgresDsn:
        return PostgresDsn.build(
            scheme="postgresql",
            username=self.postgres_user,
            password=self.postgres_password,
            host=self.postgres_host,
            port=self.postgres_port,
            path=self.postgres_db
        )

settings = Settings()