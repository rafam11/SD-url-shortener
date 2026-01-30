from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from app.clients.kgs import KGSClient
from app.core.config import Settings
from httpx import AsyncClient, HTTPError


@pytest.fixture
def mock_settings() -> Settings:
    """Mock settings for testing."""
    mock = MagicMock(spec=Settings)
    mock.kgs_url = "http://localhost:8080"
    return mock


@pytest.fixture
def mock_async_client():
    """Mock AsyncClient"""
    with patch("app.clients.kgs.AsyncClient") as mock:
        yield mock


@pytest.fixture(autouse=True)
async def reset_kgs_client():
    """Reset KGSClient state before and after each test."""
    KGSClient._client = None
    yield
    if KGSClient._client is not None:
        try:
            await KGSClient.close_client()
        except Exception:
            KGSClient._client = None


class TestKGSClient:
    """Tests for KGSClient class."""

    async def test_start_client(self, mock_settings: Settings, mock_async_client):
        "Test successful client initialization."
        mock_instance = AsyncMock(spec=AsyncClient)
        mock_response = MagicMock()
        mock_response.raise_for_status = MagicMock()
        mock_instance.get = AsyncMock(return_value=mock_response)
        mock_async_client.return_value = mock_instance

        await KGSClient.start_client(mock_settings)

        mock_async_client.assert_called_once_with(base_url=str(mock_settings.kgs_url))
        mock_response.raise_for_status.assert_called_once()
        assert KGSClient._client is mock_instance

    async def test_start_client_already_initialized(
        self, mock_settings: Settings, mock_async_client
    ):
        """Test that start_client method does not reinitialize if client already exists."""
        existing_client = AsyncMock(spec=AsyncClient)
        KGSClient._client = existing_client

        await KGSClient.start_client(mock_settings)

        mock_async_client.assert_not_called()
        assert KGSClient._client is existing_client

    async def test_start_client_error(self, mock_settings: Settings, mock_async_client):
        """Test client intialization when connection failure."""
        mock_instance = AsyncMock(spec=AsyncClient)
        mock_instance.get = AsyncMock(side_effect=HTTPError(""))
        mock_instance.aclose = AsyncMock()
        mock_async_client.return_value = mock_instance

        with pytest.raises(RuntimeError) as e:
            await KGSClient.start_client(mock_settings)

        mock_instance.aclose.assert_called_once()
        assert "Key Generation Service cannot be reached" in str(e.value)
        assert KGSClient._client is None

    async def test_get_client(self, mock_settings: Settings):
        """Test get_client returns client when it is initialized."""
        with patch("app.clients.kgs.AsyncClient") as mock_async_client:
            mock_instance = AsyncMock(spec=AsyncClient)
            mock_response = MagicMock()
            mock_response.raise_for_status = MagicMock()
            mock_instance.get = AsyncMock(return_value=mock_response)
            mock_async_client.return_value = mock_instance

            await KGSClient.start_client(mock_settings)

        client = KGSClient.get_client()
        assert client is mock_instance
        assert isinstance(client, AsyncClient)

    def test_get_client_error(self):
        """Test get_client returns client when it has not been initialized."""
        KGSClient._client = None

        with pytest.raises(RuntimeError) as e:
            KGSClient.get_client()

        assert "Key Generation Service client has not been initialized" in str(e)

    async def test_close_client(self, mock_settings: Settings):
        """Test closing an initialized client."""
        with patch("app.clients.kgs.AsyncClient") as mock_async_client:
            mock_instance = AsyncMock(spec=AsyncClient)
            mock_response = MagicMock()
            mock_response.raise_for_status = MagicMock()
            mock_instance.get = AsyncMock(return_value=mock_response)
            mock_instance.aclose = AsyncMock()
            mock_async_client.return_value = mock_instance

            await KGSClient.start_client(mock_settings)
            await KGSClient.close_client()

            mock_instance.aclose.assert_called_once()
            assert KGSClient._client is None
