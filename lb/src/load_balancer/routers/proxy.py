import logging
from http import HTTPMethod
from typing import Annotated

import httpx
from fastapi import APIRouter, Depends, HTTPException, Request, Response, status

from load_balancer.dependencies import get_load_balancer
from load_balancer.utils.load_balancer import LoadBalancer
from load_balancer.utils.server import Server

logger = logging.getLogger(__name__)

router: APIRouter = APIRouter(prefix="", tags=["proxy"])


@router.api_route(
    path="/{path:path}",
    response_model=None,
    summary="Proxy requests",
    description="Forward incoming requests to the next selected backend server",
    methods=[
        HTTPMethod.GET,
        HTTPMethod.POST,
        HTTPMethod.PUT,
        HTTPMethod.DELETE,
        HTTPMethod.PATCH,
    ],
)
async def proxy(
    path: str,
    request: Request,
    balancer: Annotated[LoadBalancer, Depends(get_load_balancer)],
):
    body = await request.body()

    async def forward(server: Server) -> httpx.Response:
        url = f"http://{server.address}/{path}"
        async with httpx.AsyncClient() as client:
            response = await client.request(
                method=request.method,
                url=url,
                content=body,
                headers=dict(request.headers),
                params=dict(request.query_params),
            )
        logger.info(
            "Request forwarded: method=%s, path=%s, server=%s, status=%d",
            request.method,
            path,
            server.address,
            response.status_code,
        )
        return response

    try:
        response = await balancer.handle_request(forward)
        return Response(
            content=response.content,
            status_code=response.status_code,
            headers=dict(response.headers),
            media_type=response.headers.get("content-type"),
        )
    except ValueError as e:
        logger.error("No healthy servers available: path=%s", path)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="No healthy servers available",
        )
    except httpx.TimeoutException as e:
        logger.warning("Server timed out: path=%s, server=%s", path, str(e))
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT, detail="Gateway timeout"
        )
    except (httpx.ConnectError, httpx.RequestError) as e:
        logger.warning("Server unreachable: path=%s, error=%s", path, str(e))
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY, detail="Bad gateway"
        )
