from functools import lru_cache

from pydantic import HttpUrl, MongoDsn, PostgresDsn
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    postgres_db: str
    postgres_user: str
    postgres_password: str
    postgres_host: str
    postgres_port: int

    secret_key: str

    mongo_db: str
    mongo_user: str
    mongo_password: str
    mongo_host: str
    mongo_port: int

    kgs_host: str
    kgs_port: int

    @property
    def postgres_uri(self) -> PostgresDsn:
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=self.postgres_user,
            password=self.postgres_password,
            host=self.postgres_host,
            port=self.postgres_port,
            path=self.postgres_db,
        )

    @property
    def mongo_uri(self) -> MongoDsn:
        return MongoDsn.build(
            scheme="mongodb",
            username=self.mongo_user,
            password=self.mongo_password,
            host=self.mongo_host,
            port=self.mongo_port,
            path=self.mongo_db,
        )

    @property
    def kgs_url(self) -> HttpUrl:
        return HttpUrl.build(
            scheme="http",
            host=self.kgs_host,
            port=self.kgs_port,
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()
