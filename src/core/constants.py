from enum import StrEnum

# Auth constants
WWW_AUTH_HEADER = "WWW-Authenticate"
BEARER_AUTH = "Bearer"
DEFAULT_EXPIRE_JWT_TOKEN = 30
HMAC_SHA256_ALGORITHM = "HS256"

# Database constants
SQLALCHEMY_BOOL_TRUE = "true"
SQLALCHEMY_BOOL_FALSE = "false"
SQLALCHEMY_KEYWORD_CASCADE = "CASCADE"
SQLALCHEMY_DELETE_ORPHAN_CASCADE = "all, delete-orphan"


class HTTPMethod(StrEnum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"


class ContentType(StrEnum):
    JSON = "application/json"
    XML = "application/xml"
