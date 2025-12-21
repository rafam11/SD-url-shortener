from fastapi import APIRouter, Depends, status

from pymongo import AsyncMongoClient

from src.api.services.urls import URLsService
from src.auth.helpers.security import verify_access_token
from src.db.schemas.url import LongUrlRequest, ShortUrlResponse
from src.db.session import MongoClient


router: APIRouter = APIRouter(prefix="/urls", tags=["urls"])


@router.post(
    path="/shorten/",
    response_model=ShortUrlResponse,
    status_code=status.HTTP_200_OK,
    summary="Shorten a URL",
    description="",
)
async def short_url(
    long_url: LongUrlRequest,
    user_id: str = Depends(verify_access_token),
    client: AsyncMongoClient = Depends(MongoClient.get_client),
):
    return await URLsService(client).shorten_url(user_id, long_url)
