from contextlib import asynccontextmanager
from fastapi import FastAPI

from api.core import constants as cons
from api.clients.kgs import KGSClient
from api.clients.mongo import MongoClient
from api.clients.postgres import session_manager
from api.routers.users import router as users_router
from api.routers.urls import router as urls_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    session_manager.run_engine()
    await MongoClient.start_client()
    await KGSClient.start_client()
    yield
    await session_manager.close()
    await MongoClient.close_client()
    await KGSClient.close_client()


app = FastAPI(lifespan=lifespan)
app.include_router(users_router, prefix=cons.API_V1_PREFIX)
app.include_router(urls_router, prefix=cons.API_V1_PREFIX)
