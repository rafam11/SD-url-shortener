from contextlib import asynccontextmanager

from fastapi import FastAPI

from load_balancer.core.config import get_settings
from load_balancer.routers import health, proxy
from load_balancer.utils.load_balancer import RoundRobinBalancer


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    servers = settings.get_servers()
    app.state.load_balancer = RoundRobinBalancer(servers=servers)
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(health.router)
app.include_router(proxy.router)
