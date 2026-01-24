from pymongo import AsyncMongoClient

from api.models.pydantic import URLModel
from api.repositories.base import BaseMongoRepository


class URLRepository(BaseMongoRepository):
    collection_name = "urls"

    def __init__(self, client: AsyncMongoClient, database_name: str):
        super().__init__(
            client=client,
            model_class=URLModel,
            database_name=database_name,
        )
