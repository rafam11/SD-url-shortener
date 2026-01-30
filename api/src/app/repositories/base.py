from typing import Any, Generic, TypeVar

from pydantic import BaseModel
from pymongo import AsyncMongoClient
from pymongo.errors import DuplicateKeyError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.clients.base import Base
from app.core import constants as cons
from app.core.errors import RecordAlreadyExists
from app.utils.retry import retry

SQLAlchemyModelType = TypeVar("SQLAlchemyModelType", bound=Base)
PydanticModelType = TypeVar("PydanticModelType", bound=BaseModel)


class BaseRepository(Generic[SQLAlchemyModelType]):
    """
    A generic SQLAlchemy repository providing basic CRUD operations for SQLAlchemy ORM models.

    Class is meant to be subclassed for specific models.
    """

    def __init__(
        self,
        session: AsyncSession,
    ):
        self.session = session

    async def create(self, model: SQLAlchemyModelType) -> SQLAlchemyModelType:
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return model

    async def retrieve_by(
        self, model: type[SQLAlchemyModelType], **filters: Any
    ) -> SQLAlchemyModelType | None:
        for key, _ in filters.items():
            if not hasattr(model, key):
                raise ValueError(f"Model {model.__name__} has no attribute {key}")

        stmt = select(model).filter_by(**filters)
        return await self.session.scalar(stmt)


class BaseMongoRepository(Generic[PydanticModelType]):
    """
    A generic repository providing basic operations for interacting with MongoDB database.

    Class is meant to be subclasses for specific models.
    """

    collection_name: str

    def __init__(
        self,
        client: AsyncMongoClient,
        model_class: type[PydanticModelType],
        database_name: str,
    ):
        self.client = client
        self.model_class = model_class
        self.database = client.get_database(database_name)
        self.collection = self.database.get_collection(self.collection_name)

    @retry(times=cons.NUM_RETRIES_BEFORE_FAILING)
    async def insert(self, model: PydanticModelType) -> PydanticModelType:
        new_record = model.model_dump(by_alias=True, exclude={"id"})
        try:
            result = await self.collection.insert_one(new_record)
            new_record["_id"] = result.inserted_id
            return self.model_class.model_validate(new_record)
        except DuplicateKeyError as e:
            raise RecordAlreadyExists() from e

    @retry(times=cons.NUM_RETRIES_BEFORE_FAILING)
    async def retrieve_by(self, filters: Any) -> PydanticModelType | None:
        document = await self.collection.find_one(filters)
        if not document:
            return None
        return self.model_class.model_validate(document)
