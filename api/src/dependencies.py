from fastapi import Depends
from httpx import AsyncClient
from pymongo import AsyncMongoClient
from sqlalchemy.ext.asyncio import AsyncSession

from src.clients.kgs import KGSClient
from src.clients.mongo import MongoClient
from src.clients.postgres import session_manager
from src.services.users import UserService
from src.services.urls import URLService
from src.services.kgs import KGSService


def get_user_service(
    session: AsyncSession = Depends(session_manager.get_session),
) -> UserService:
    return UserService(session)


def get_kgs_service(
    client: AsyncClient = Depends(KGSClient.get_client),
) -> KGSService:
    return KGSService(client)


def get_url_service(
    client: AsyncMongoClient = Depends(MongoClient.get_client),
    kgs_service: KGSService = Depends(get_kgs_service),
) -> URLService:
    return URLService(client, kgs_service)
