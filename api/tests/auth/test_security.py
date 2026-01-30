from unittest.mock import MagicMock

import app.core.constants as cons
import jwt
import pytest
from app.auth.security import (
    create_access_token,
    get_password_hash,
    verify_access_token,
    verify_password,
)
from app.core.config import Settings
from fastapi import HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials


@pytest.fixture
def mock_settings() -> Settings:
    """Mock settings for testing."""
    return MagicMock(spec=Settings, secret_key="test_secret_key")


@pytest.fixture
def valid_credentials() -> HTTPAuthorizationCredentials:
    """Valid HTTP credentials fixture."""
    return HTTPAuthorizationCredentials(scheme="Bearer", credentials="valid_token")


@pytest.fixture
def plain_password() -> str:
    """Plain test password for testing."""
    return "MyPassword123"


@pytest.fixture
def hashed_password(plain_password: str) -> str:
    return get_password_hash(plain_password)


@pytest.fixture
def user_id() -> int:
    """Test user ID."""
    return 1


@pytest.fixture
def secret_key() -> str:
    """Test secret key for JWT."""
    return "test_secret_key"


class TestPasswordHashing:
    """Tests for password hashing and verification."""

    def test_get_password_hash(self, plain_password: str):
        """Test simple password hashing encoding."""
        hashed = get_password_hash(plain_password)
        assert isinstance(hashed, str)
        assert len(hashed) > 0

    def test_get_password_hash_salt(self, plain_password: str):
        """Test that same passwords produces different hashes due to salt."""
        hash_1 = get_password_hash(plain_password)
        hash_2 = get_password_hash(plain_password)
        assert hash_1 != hash_2

    def test_verify_password_ok(self, plain_password: str, hashed_password: str):
        """Test password verification with right password."""
        assert verify_password(plain_password, hashed_password) is True

    def test_verify_password_ko(self, hashed_password: str):
        """Test password verification with wrong password."""
        assert verify_password("WrongPassword123", hashed_password) is False


class TestCreateAccessToken:
    """Test for JWT token creation."""

    def test_create_access_token(self, user_id: int, secret_key: str):
        """Test token creation with custom expiration."""
        expires_delta = 60
        token = create_access_token(
            user_id=user_id, secret_key=secret_key, expires_delta=expires_delta
        )
        payload = jwt.decode(
            jwt=token, key=secret_key, algorithms=[cons.HMAC_SHA256_ALGORITHM]
        )
        assert isinstance(token, bytes)
        assert payload["sub"] == str(user_id)


class TestVerifyAccessToken:
    """Tests for JWT token verification."""

    async def test_verify_access_token(self, mock_settings: Settings, user_id: int):
        """Test token verification with valid token."""
        token = create_access_token(
            user_id=user_id, secret_key=mock_settings.secret_key
        )
        credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials=token)
        verified_user_id = await verify_access_token(
            settings=mock_settings, credentials=credentials
        )

        assert verified_user_id == str(user_id)

    async def test_verify_access_token_invalid(self, mock_settings: Settings):
        """Test token verification with an invalid token."""
        credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials="")
        with pytest.raises(HTTPException) as e:
            await verify_access_token(settings=mock_settings, credentials=credentials)

        assert e.value.status_code == status.HTTP_401_UNAUTHORIZED
