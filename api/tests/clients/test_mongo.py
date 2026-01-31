from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from app.clients.mongo import MongoClient
from app.core.config import Settings
from pymongo import AsyncMongoClient
from pymongo.errors import ConnectionFailure


@pytest.fixture
def mock_settings() -> Settings:
    """Mock settings for testing."""
    mock = MagicMock(spec=Settings)
    mock.mongo_uri = "mongodb://localhost:27017"
    return mock


@pytest.fixture
def mock_async_client():
    """Mock AsyncMongoClient"""
    with patch("app.clients.mongo.AsyncMongoClient") as mock:
        yield mock


@pytest.fixture(autouse=True)
async def reset_mongo_client():
    """Reset MongoClient state before and after each test."""
    MongoClient._client = None
    yield
    if MongoClient._client is not None:
        try:
            await MongoClient.close_client()
        except Exception:
            MongoClient._client = None


class TestMongoClient:
    """Tests for KGSClient class."""

    async def test_start_client(self, mock_settings: Settings, mock_async_client):
        "Test successful client initialization."
        mock_instance = AsyncMock(spec=AsyncMongoClient)
        mock_admin = MagicMock()
        mock_admin.command = AsyncMock(return_value={"ok": 1})
        mock_instance.admin = mock_admin
        mock_async_client.return_value = mock_instance

        await MongoClient.start_client(mock_settings)

        mock_async_client.assert_called_once_with(host=str(mock_settings.mongo_uri))
        mock_admin.command.assert_called_once_with("ping")
        assert MongoClient._client is mock_instance

    async def test_start_client_already_initialized(
        self, mock_settings: Settings, mock_async_client
    ):
        """Test that start_client method does not reinitialize if client already exists."""
        existing_client = AsyncMock(spec=AsyncMongoClient)
        MongoClient._client = existing_client

        await MongoClient.start_client(mock_settings)

        mock_async_client.assert_not_called()
        assert MongoClient._client is existing_client

    async def test_start_client_error(self, mock_settings: Settings, mock_async_client):
        """Test client intialization when connection failure."""
        mock_instance = AsyncMock(spec=AsyncMongoClient)
        mock_admin = MagicMock()
        mock_admin.command = AsyncMock(side_effect=ConnectionFailure)
        mock_instance.admin = mock_admin
        mock_instance.close = AsyncMock()
        mock_async_client.return_value = mock_instance

        with pytest.raises(RuntimeError) as e:
            await MongoClient.start_client(mock_settings)

        mock_instance.close.assert_called_once()
        assert "MongoDB connection failed during startup" in str(e.value)
        assert MongoClient._client is None

    async def test_get_client(self, mock_settings: Settings):
        """Test get_client returns client when it is initialized."""
        with patch("app.clients.mongo.AsyncMongoClient") as mock_async_client:
            mock_instance = AsyncMock(spec=AsyncMongoClient)
            mock_admin = MagicMock()
            mock_admin.command = AsyncMock(return_value={"ok": 1})
            mock_instance.admin = mock_admin
            mock_async_client.return_value = mock_instance

            await MongoClient.start_client(mock_settings)

        client = MongoClient.get_client()
        assert client is mock_instance
        assert isinstance(client, AsyncMongoClient)

    async def test_get_client_error(self):
        """Test get_client returns client when it has not been initialized."""
        MongoClient._client = None

        with pytest.raises(RuntimeError) as e:
            MongoClient.get_client()

        assert "MongoDB client has not been initialized" in str(e)

    async def test_close_client(self, mock_settings: Settings):
        """Test closing an initialized client."""
        with patch("app.clients.mongo.AsyncMongoClient") as mock_async_client:
            mock_instance = AsyncMock(spec=AsyncMongoClient)
            mock_instance = AsyncMock(spec=AsyncMongoClient)
            mock_admin = MagicMock()
            mock_admin.command = AsyncMock(return_value={"ok": 1})
            mock_instance.admin = mock_admin
            mock_instance.close = AsyncMock()
            mock_async_client.return_value = mock_instance

            await MongoClient.start_client(mock_settings)
            await MongoClient.close_client()

            mock_instance.close.assert_called_once()
            assert MongoClient._client is None
