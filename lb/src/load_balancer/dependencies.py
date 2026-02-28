from fastapi import Request

from load_balancer.utils.load_balancer import RoundRobinBalancer


def get_load_balancer(request: Request) -> RoundRobinBalancer:
    return request.app.state.load_balancer
