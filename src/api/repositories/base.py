from sqlalchemy.ext.asyncio import AsyncSession
from src.db.base import Base

from typing import Generic, TypeVar

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

    async def create(
        self, 
        model: ModelType
    ) -> ModelType:
        self.session.add(model)
        self.session.commit()
        self.session.refresh(model)
        return model
