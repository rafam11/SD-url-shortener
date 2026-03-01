import asyncio
import logging

import httpx

from load_balancer.core import constants as lb_cons
from load_balancer.utils.server import Server

logger = logging.getLogger(__name__)


async def restore_servers(
    servers: list[Server], interval: int = lb_cons.HealthCheck.INTERVAL
) -> None:
    """Periodically check unhealthy servers and mark them healthy if restored."""
    while True:
        await asyncio.sleep(interval)
        for server in servers:
            if not server.healthy:
                try:
                    async with httpx.AsyncClient() as client:
                        await client.get(
                            url=f"http://{server.address}/health",
                            timeout=lb_cons.HealthCheck.TIMEOUT,
                        )
                    await server.set_healthy()
                    logger.info("Server recovered: address=%s", server.address)
                except httpx.RequestError:
                    pass
