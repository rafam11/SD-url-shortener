from typing import Generator
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from app.main import app, lifespan


@pytest.fixture
def mock_settings() -> Generator[MagicMock, None, None]:
    mock = MagicMock()
    mock.postgres_db = "test_db"
    mock.postgres_user = "test_user"
    mock.postgres_password = "test_password"
    mock.postgres_host = "localhost"
    mock.postgres_port = 5432
    mock.secret_key = "test_secret_key"
    mock.mongo_db = "test_mongo_db"
    mock.mongo_user = "test_mongo_user"
    mock.mongo_password = "test_mongo_password"
    mock.mongo_host = "localhost"
    mock.mongo_port = 27017
    mock.kgs_host = "localhost"
    mock.kgs_port = 8080

    with patch("api.main.get_settings", return_value=mock):
        yield mock


@pytest.fixture
def mock_session_manager() -> Generator[MagicMock, None, None]:
    with patch("api.main.SessionManager") as mock:
        mock.run_engine = MagicMock()
        mock.close = AsyncMock()
        yield mock


@pytest.fixture
def mock_mongo_client() -> Generator[MagicMock, None, None]:
    with patch("api.main.MongoClient") as mock:
        mock.start_client = AsyncMock()
        mock.close_client = AsyncMock()
        yield mock


@pytest.fixture
def mock_kgs_client() -> Generator[MagicMock, None, None]:
    with patch("api.main.KGSClient") as mock:
        mock.start_client = AsyncMock()
        mock.close_client = AsyncMock()
        yield mock


class TestLifespan:
    """Test the FastAPI lifespan context manager"""

    @pytest.mark.asyncio
    async def test_lifespan_startup(
        self,
        mock_settings: MagicMock,
        mock_session_manager: MagicMock,
        mock_mongo_client: MagicMock,
        mock_kgs_client: MagicMock,
    ):
        async with lifespan(app):
            mock_session_manager.run_engine.assert_called_once()
            mock_mongo_client.start_client.assert_called_once()
            mock_kgs_client.start_client.assert_called_once()

    @pytest.mark.asyncio
    async def test_lifespan_shutdown(
        self,
        mock_settings: MagicMock,
        mock_session_manager: MagicMock,
        mock_mongo_client: MagicMock,
        mock_kgs_client: MagicMock,
    ):
        async with lifespan(app):
            pass

        mock_session_manager.close.assert_called_once()
        mock_mongo_client.close_client.assert_called_once()
        mock_kgs_client.close_client.assert_called_once()
