from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from pymongo import AsyncMongoClient

from src.api.services.urls import URLService
from src.auth.helpers.security import verify_access_token
from src.core.errors import URLNotFoundException, RecordAlreadyExists
from src.db.schemas.url import LongUrlRequest, ShortUrlResponse
from src.db.session import MongoClient

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
    client: AsyncMongoClient = Depends(MongoClient.get_client),
):
    try:
        return await URLService(client).shorten_url(user_id, long_url)
    except RecordAlreadyExists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="URL already exists"
        )


@router.get(path="/{short_url}")
async def redirect(
    short_url: str, client: AsyncMongoClient = Depends(MongoClient.get_client)
):
    try:
        long_url = await URLService(client).retrieve_long_url(short_url)
        return RedirectResponse(
            url=long_url, status_code=status.HTTP_301_MOVED_PERMANENTLY
        )
    except URLNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="URL not found"
        )
