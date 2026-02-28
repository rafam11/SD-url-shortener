from typing import Annotated

from fastapi import APIRouter, Depends

from load_balancer.dependencies import get_load_balancer
from load_balancer.utils.load_balancer import LoadBalancer

router = APIRouter(tags=["Monitoring"])


@router.get("/health")
def health(load_balancer: Annotated[LoadBalancer, Depends(get_load_balancer)]):
    """Return the current status of all servers in the pool."""
    return {
        "servers": [
            {
                "address": server.address,
                "healthy": server.healthy,
                "connections": server.connections,
            }
            for server in load_balancer.servers
        ]
    }
