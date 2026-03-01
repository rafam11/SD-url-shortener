import httpx
from fastapi import FastAPI, HTTPException, status

app = FastAPI()


@app.get("/key")
async def generate_key():
    """Request a key from the load balancer."""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get("http://load_balancer:8080/key")
            return response.json()
        except httpx.RequestError:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Token service unavailable",
            )


@app.get("/health", status_code=status.HTTP_200_OK)
def health():
    return {"status": "ok"}
