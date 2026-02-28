from typing import Annotated

import httpx
from fastapi import APIRouter, Depends, HTTPException, Request, Response

from load_balancer.dependencies import get_load_balancer
from load_balancer.utils.load_balancer import LoadBalancer
from load_balancer.utils.server import Server

router = APIRouter(tags=["Proxy"])


@router.api_route(
    path="/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"]
)
async def proxy(
    path: str,
    request: Request,
    load_balancer: Annotated[LoadBalancer, Depends(get_load_balancer)],
):
    """Forward incoming requests to the next selected backend server."""
    try:
        body = await request.body()

        def forward(server: Server) -> httpx.Response:
            url = f"http://{server.address}/{path}"
            with httpx.Client() as client:
                return client.request(
                    method=request.method,
                    url=url,
                    headers=dict(request.headers),
                    content=body,
                    params=dict(request.query_params),
                )

        response = load_balancer.handle_request(forward)
        return Response(
            content=response.content,
            status_code=response.status_code,
            headers=dict(response.headers),
            media_type=response.headers.get("content-type"),
        )
    except ValueError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except httpx.RequestError as e:
        raise HTTPException(status_code=502, detail=str(e))
