from enum import StrEnum


class LoadBalancingAlgorithms(StrEnum):
    ROUND_ROBIN = "round_robin"
    LEAST_CONNECTIONS = "least_connections"
