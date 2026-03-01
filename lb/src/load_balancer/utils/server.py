import asyncio
from dataclasses import dataclass, field


@dataclass
class Server:
    """
    Represents a backend server in the load balancer pool.

    Attributes:
        host: The host name or IP address of the server
        port: The port number where the server is listening on
        connections: Current number of active connections
        healthy: Whether the server is healthy and can accept requests
    """

    host: str
    port: int
    connections: int = 0
    healthy: bool = True
    _lock: asyncio.Lock = field(init=False, repr=False)

    def __post_init__(self):
        self._lock = asyncio.Lock()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Server):
            return NotImplemented
        return self.host == other.host and self.port == other.port

    async def increment_connections(self):
        """
        Thread-safe increment of active connection count.
        Called when a new request is routed to this server.
        """
        async with self._lock:
            self.connections += 1

    async def decrement_connections(self):
        """
        Thread-safe decrement of active connection count.
        Called when a request completes or connection closes.
        """
        async with self._lock:
            if self.connections > 0:
                self.connections -= 1

    async def set_healthy(self):
        async with self._lock:
            self.healthy = True

    async def set_unhealthy(self):
        async with self._lock:
            self.healthy = False

    @property
    def address(self) -> str:
        """Returns the full address of the server."""
        return f"{self.host}:{self.port}"
