import json
import logging
import logging.config
from contextlib import asynccontextmanager

from fastapi import FastAPI

from load_balancer.core.config import get_settings
from load_balancer.routers import health, proxy
from load_balancer.utils.load_balancer import RoundRobinBalancer

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()

    logger_config = json.loads(settings.logger_config_path.read_text())
    logging.config.dictConfig(logger_config)

    servers = settings.get_servers()
    app.state.load_balancer = RoundRobinBalancer(servers=servers)

    logger.info(
        "Load balancer started: algorithm=%s, num_servers=%d",
        app.state.load_balancer.algorithm,
        len(servers),
    )
    for server in servers:
        logger.info("Server started: address=%s", server.address)
    yield
    logger.info("Load balancer shutting down")


app = FastAPI(lifespan=lifespan)
app.include_router(health.router)
app.include_router(proxy.router)
