from fastapi import Depends
from httpx import AsyncClient
from pymongo import AsyncMongoClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.clients.kgs import KGSClient
from app.clients.mongo import MongoClient
from app.clients.postgres import SessionManager
from app.core.config import Settings, get_settings
from app.services.kgs import KGSService
from app.services.urls import URLService
from app.services.users import UserService


def get_user_service(
    session: AsyncSession = Depends(SessionManager.get_session),
) -> UserService:
    return UserService(session)


def get_kgs_service(
    client: AsyncClient = Depends(KGSClient.get_client),
) -> KGSService:
    return KGSService(client)


def get_url_service(
    client: AsyncMongoClient = Depends(MongoClient.get_client),
    settings: Settings = Depends(get_settings),
    kgs_service: KGSService = Depends(get_kgs_service),
) -> URLService:
    return URLService(
        client=client, database_name=settings.mongo_db, kgs_service=kgs_service
    )
