from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.api.controllers.users import router as users_router
from src.db.session import session_manager

@asynccontextmanager
async def lifespan(app: FastAPI):
    session_manager.run_engine()
    yield
    await session_manager.close()

app = FastAPI(lifespan=lifespan)
app.include_router(users_router)
