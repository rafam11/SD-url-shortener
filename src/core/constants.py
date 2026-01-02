from enum import StrEnum

# Auth constants
WWW_AUTH_HEADER = "WWW-Authenticate"
BEARER_AUTH = "Bearer"
DEFAULT_EXPIRE_JWT_TOKEN = 10
HMAC_SHA256_ALGORITHM = "HS256"

# Database constants
SQLALCHEMY_BOOL_TRUE = "true"
SQLALCHEMY_BOOL_FALSE = "false"
SQLALCHEMY_KEYWORD_CASCADE = "CASCADE"
SQLALCHEMY_DELETE_ORPHAN_CASCADE = "all, delete-orphan"

# MongoDB constants
NUM_RETRIES_BEFORE_FAILING = 3
BACKOFF_FACTOR = 0.2


class HTTPMethod(StrEnum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"


class ContentType(StrEnum):
    JSON = "application/json"
    XML = "application/xml"
