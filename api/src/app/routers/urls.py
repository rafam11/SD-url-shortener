from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse

from app.auth.security import verify_access_token
from app.core.errors import (
    KeyGenerationError,
    RecordAlreadyExists,
    URLNotFoundException,
)
from app.dependencies import get_url_service
from app.schemas.url import LongUrlRequest, ShortUrlResponse
from app.services.urls import URLService

router: APIRouter = APIRouter(prefix="/urls", tags=["urls"])


@router.post(
    path="/shorten/",
    response_model=ShortUrlResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Shorten a URL",
    description="This endpoint accepts a long URL and returns a shortened version. User authentication is required.",
)
async def short_url(
    long_url: LongUrlRequest,
    user_id: str = Depends(verify_access_token),
    service: URLService = Depends(get_url_service),
):
    try:
        return await service.shorten_url(user_id, long_url)
    except RecordAlreadyExists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="URL already exists"
        )
    except KeyGenerationError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Key generation service unavailable",
        )


@router.get(path="/{short_url}")
async def redirect(
    short_url: str,
    service: URLService = Depends(get_url_service),
):
    try:
        long_url = await service.retrieve_long_url(short_url)
        return RedirectResponse(
            url=long_url, status_code=status.HTTP_301_MOVED_PERMANENTLY
        )
    except URLNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="URL not found"
        )
