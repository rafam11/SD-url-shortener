from typing import ClassVar

from httpx import AsyncClient, HTTPError

from app.core.config import Settings


class KGSClient:
    """Client for communicating with Key Generation Service."""

    _client: ClassVar[AsyncClient | None] = None

    @classmethod
    async def start_client(cls, settings: Settings):
        """Initialize the HTTP client and verify connection."""
        if cls._client is not None:
            return
        try:
            client = AsyncClient(base_url=str(settings.kgs_url))
            response = await client.get("/health")
            response.raise_for_status()
            cls._client = client
        except HTTPError as exc:
            await client.aclose()
            raise RuntimeError(
                f"Key Generation Service cannot be reached: {exc}"
            ) from exc

    @classmethod
    def get_client(cls) -> AsyncClient:
        if cls._client is None:
            raise RuntimeError("Key Generation Service client has not been initialized")
        return cls._client

    @classmethod
    async def close_client(cls):
        if cls._client is not None:
            await cls._client.aclose()
            cls._client = None
