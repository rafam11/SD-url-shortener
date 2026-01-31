import os

import httpx
from fastapi import FastAPI

from load_balancer.utils.strategy import (
    LoadBalancer,
    RoundRobinStrategy,
)

app = FastAPI()

servers = [s.strip() for s in os.getenv("SERVERS", "").split(",") if s.strip()]
lb = LoadBalancer(servers, RoundRobinStrategy())


@app.get("/key")
async def get_key():
    server = lb.get_next_server()
    async with httpx.AsyncClient() as client:
        response = await client.get(f"http://{server}/key")
    return response.json()


@app.get("/health")
async def health():
    return {"status": "ok"}
