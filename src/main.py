from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.api.controllers.users import router as users_router
from src.api.controllers.urls import router as urls_router
from src.db.session import MongoClient, session_manager


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
