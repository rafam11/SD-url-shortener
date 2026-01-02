from pymongo import AsyncMongoClient
from src.api.repositories.base import BaseMongoRepository
from src.db.models.pydantic import URLModel
from src.db.utils.settings import settings


class URLRepository(BaseMongoRepository):
    collection_name = "urls"

    def __init__(self, client: AsyncMongoClient):
        super().__init__(
            client=client,
            model_class=URLModel,
            database_name=settings.mongo_db,
        )
