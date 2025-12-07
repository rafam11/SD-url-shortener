from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.api.controllers.users import router as users_router
from src.db.session import SessionManager

session_manager = SessionManager()

@asynccontextmanager
async def lifespan(app: FastAPI):
    session_manager.run_engine()
    yield
    session_manager.close()

app = FastAPI(lifespan=lifespan)
app.include_router(users_router)
