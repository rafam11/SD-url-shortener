class InvalidCredentialsError(Exception):
    """Exception raised when user authentication fails."""


class URLNotFoundException(Exception):
    """Exception raised when a short URL does not exist in the repository."""


class RecordAlreadyExists(Exception):
    """Exception raised when a record already exists in the database."""


class KeyGenerationError(Exception):
    """Exception raised when short URL cannot be created."""
