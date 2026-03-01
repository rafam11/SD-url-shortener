from enum import StrEnum


class LoadBalancingAlgorithms(StrEnum):
    ROUND_ROBIN = "round_robin"
    LEAST_CONNECTIONS = "least_connections"


class HealthCheck:
    TIMEOUT: int = 2
    INTERVAL: int = 10
