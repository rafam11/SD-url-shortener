from pymongo import AsyncMongoClient
from src.core.config import settings
from src.models.pydantic import URLModel
from src.repositories.base import BaseMongoRepository


class URLRepository(BaseMongoRepository):
    collection_name = "urls"

    def __init__(self, client: AsyncMongoClient):
        super().__init__(
            client=client,
            model_class=URLModel,
            database_name=settings.mongo_db,
        )
