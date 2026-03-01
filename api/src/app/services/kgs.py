from httpx import AsyncClient, HTTPStatusError, RequestError

from app.core.errors import KeyGenerationError


class KGSService:
    """Service for interacting with Key Generation Service."""

    def __init__(self, client: AsyncClient):
        self.client = client

    async def get_short_url_key(self) -> str:
        try:
            response = await self.client.get("/key")
            response.raise_for_status()
            return response.json()["key"]
        except (HTTPStatusError, RequestError) as e:
            raise KeyGenerationError() from e
