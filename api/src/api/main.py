from contextlib import asynccontextmanager

from fastapi import FastAPI

from api.clients.kgs import KGSClient
from api.clients.mongo import MongoClient
from api.clients.postgres import SessionManager
from api.core import constants as cons
from api.core.config import get_settings
from api.routers.urls import router as urls_router
from api.routers.users import router as users_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    SessionManager.run_engine(settings)
    await MongoClient.start_client(settings)
    await KGSClient.start_client(settings)
    yield
    await SessionManager.close()
    await MongoClient.close_client()
    await KGSClient.close_client()


app = FastAPI(lifespan=lifespan)
app.include_router(users_router, prefix=cons.API_V1_PREFIX)
app.include_router(urls_router, prefix=cons.API_V1_PREFIX)
