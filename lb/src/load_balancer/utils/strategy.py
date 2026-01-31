import random
import threading
from abc import ABC, abstractmethod


class LoadBalancingStrategy(ABC):
    """Abstract base class for load balancing strategies."""

    @abstractmethod
    def select_server(self, servers: list[str], **kwargs) -> str:
        """Select a server based on the strategy."""
        pass


class RoundRobinStrategy(LoadBalancingStrategy):
    """Round-robin load balancing strategy."""

    def __init__(self):
        self.current_index = 0
        self.lock = threading.Lock()

    def select_server(self, servers: list[str], **kwargs) -> str:
        """Select server in round-robin way."""
        with self.lock:
            server = servers[self.current_index]
            self.current_index = (self.current_index + 1) % len(servers)
            return server


class LeastConnectionsStrategy(LoadBalancingStrategy):
    """Least connections load balancing strategy."""

    def __init__(self):
        self.connections = {}
        self.lock = threading.Lock()

    def select_server(self, servers: list[str], **kwargs) -> str:
        """Select server with least active connections."""
        with self.lock:
            for server in servers:
                if server not in self.connections:
                    self.connections[server] = 0

            server = min(servers, key=lambda s: self.connections[s])
            self.connections[server] += 1
            return server

    def complete_request(self, server: str):
        """Decrement connection count when request completes."""
        with self.lock:
            if server in self.connections and self.connections[server] > 0:
                self.connections[server] -= 1


class RandomStrategy(LoadBalancingStrategy):
    """Random server selection strategy."""

    def select_server(self, servers: list[str], **kwargs) -> str:
        return random.choice(servers)


class LoadBalancer:
    """Load Balancer base class."""

    def __init__(self, servers: list[str], strategy: LoadBalancingStrategy):
        """
        Initialize LoadBalancer

        Args:
            servers: List of backend server URLs.
            strategy: LoadBalancingStrategy instance.
        Raises:
            ValueError: If servers list is empty.
            TypeError: If strategy is not a LoadBalancingStrategy instance.

        """
        if not servers:
            raise ValueError("Server list cannot be empty.")

        if not isinstance(strategy, LoadBalancingStrategy):
            raise TypeError("Strategy must be an instance of LoadBalancingStrategy.")

        self.servers = servers
        self.strategy = strategy

    def get_next_server(self) -> str:
        """
        Get the next server based on the load balancing strategy.

        Args:

        Returns:
            Selected server URL
        """
        return self.strategy.select_server(self.servers)

    def complete_request(self, server: str):
        """
        Notify that a request to a server has completed (only relevant for LeastConnectionsStrategy).
        Args:
            server: Server URL where request completed.
        """
        if isinstance(self.strategy, LeastConnectionsStrategy):
            self.strategy.complete_request(server)
