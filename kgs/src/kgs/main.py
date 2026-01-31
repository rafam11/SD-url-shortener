import httpx
from fastapi import FastAPI, status

app = FastAPI()


@app.get("/key")
async def generate_key():
    """Request a key from the load balancer."""
    async with httpx.AsyncClient() as client:
        response = await client.get("http://load_balancer:8080/key")
    return response.json()


@app.get("/health", status_code=status.HTTP_200_OK)
def health():
    return {"status": "ok"}
