from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.base import Base

from typing import Any, Generic, TypeVar

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """
    A generic SQLAlchemy repository providing basic CRUD operations for SQLAlchemy ORM models.

    Class is meant to be subclassed for specific models.
    """

    def __init__(
        self,
        session: AsyncSession,
    ):
        self.session = session

    async def create(self, model: ModelType) -> ModelType:
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return model

    async def retrieve_by(
        self, model: type[ModelType], **filters: Any
    ) -> ModelType | None:
        for key, _ in filters.items():
            if not hasattr(model, key):
                raise ValueError(f"Model {model.__name__} has no attribute {key}")

        stmt = select(model).filter_by(**filters)
        return await self.session.scalar(stmt)
