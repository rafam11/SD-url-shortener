from pydantic import MongoDsn, PostgresDsn
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


settings = Settings()
