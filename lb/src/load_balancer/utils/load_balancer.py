import threading
from abc import ABC, abstractmethod
from typing import Any, Callable

from load_balancer.utils.server import Server


class LoadBalancer(ABC):
    """Load Balancer base class."""

    def __init__(self, servers: list[Server] | None = None):
        """Initialize the load balancer with an optional list of servers."""
        self.servers: list[Server] = servers or []
        self._lock = threading.Lock()

    def add_server(self, server: Server):
        """Add a new server to the pool."""
        with self._lock:
            self.servers.append(server)

    def remove_server(self, server: Server):
        """Remove a server from the pool."""
        with self._lock:
            self.servers = [s for s in self.servers if s != server]

    def _get_healthy_servers(self) -> list[Server]:
        """Return a list of healthy servers. This method must be called within lock context."""
        healthy_servers = [s for s in self.servers if s.healthy]
        if not healthy_servers:
            raise ValueError("No healthy servers available")
        return healthy_servers

    def get_server(self) -> Server:
        """Select the specific server based on strategy."""
        with self._lock:
            return self._select_server()

    @abstractmethod
    def _select_server(self) -> Server:
        """Must be implemented by each subclass."""
        pass

    def handle_request(self, request_handler: Callable[[Server], Any]) -> Any:
        """Route a request to the server."""
        server = self.get_server()
        server.increment_connections()
        try:
            result = request_handler(server)
            return result
        finally:
            server.decrement_connections()


class RoundRobinBalancer(LoadBalancer):
    """Round-Robin load balancer class."""

    def __init__(self, servers: list[Server] | None = None):
        super().__init__(servers)
        self.current_index = 0

    def _select_server(self) -> Server:
        """Select server in round-robin way."""
        healthy_servers = self._get_healthy_servers()
        server = healthy_servers[self.current_index % len(healthy_servers)]
        self.current_index += 1
        return server


class LeastConnectionsBalancer(LoadBalancer):
    """Least connections load balancer class."""

    def __init__(self, servers: list[Server] | None = None):
        super().__init__(servers)

    def _select_server(self) -> Server:
        """Select server with least active"""
        healthy_servers = self._get_healthy_servers()
        return min(healthy_servers, key=lambda s: s.connections)
