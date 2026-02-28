import re
from functools import lru_cache
from typing import Annotated

from pydantic import BeforeValidator
from pydantic_settings import BaseSettings

from load_balancer.utils.server import Server


def validate_servers(servers: str) -> str:
    """
    Validate that servers string is in the right format.

    Accepts:
        - String: "host:port1,host2:port2,host3:port3"
    Returns:
        - String in the format "host1:port1,host2:port2,..."
    Raises:
        ValueError: if format is invalid
    """
    if not isinstance(servers, str):
        raise ValueError("Servers must be a string")

    pattern = r"^[a-zA-Z0-9]([a-zA-Z0-9\-\.]*[a-zA-Z0-9])?:\d{1,5}$"
    for server in servers.split(","):
        if not re.match(pattern, server):
            raise ValueError(
                f"Invalid server format: {server}. "
                "Expected format: 'host:port' (e.g., 'localhost:8000')"
            )
    return servers


class Settings(BaseSettings):
    servers: Annotated[str, BeforeValidator(validate_servers)]
    load_balancer_port: int

    def get_servers(self) -> list[Server]:
        """Parse environment variable into a list of Server objects."""
        servers = []
        for server_str in self.servers.split(","):
            server_str = server_str.strip()
            host, port = server_str.split(":", 1)
            servers.append(Server(host=host, port=int(port)))
        return servers


@lru_cache
def get_settings() -> Settings:
    return Settings()
