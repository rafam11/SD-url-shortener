from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.db.mongo import MongoClient
from src.db.postgres import session_manager
from src.routers.users import router as users_router
from src.routers.urls import router as urls_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    session_manager.run_engine()
    await MongoClient.start_client()
    yield
    await session_manager.close()
    await MongoClient.close_client()


app = FastAPI(lifespan=lifespan)
app.include_router(users_router)
app.include_router(urls_router)
