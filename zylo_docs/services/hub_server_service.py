import httpx
from fastapi import HTTPException
EXTERNAL_API_BASE = "https://api.zylosystems.com"
async def get_spec_content_by_id(spec_id: str, client: httpx.AsyncClient) -> dict:
    try:
        response = await client.get(f"{EXTERNAL_API_BASE}/specs/{spec_id}")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        # handle exception and return an empty dict or error info
        return {"error": str(e)}
