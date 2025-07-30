import httpx
from fastapi import HTTPException
from zylo_docs.config import EXTERNAL_API_BASE
async def get_spec_content_by_id(spec_id: str, client: httpx.AsyncClient, access_token: str) -> dict:
    try:
        resp = await client.get(f"{EXTERNAL_API_BASE}/specs/{spec_id}", headers={"Authorization": f"Bearer {access_token}"})
        resp.raise_for_status()
        response_data = resp.json()
        spec_content = response_data.get("data", {}).get("spec_content")

        if not spec_content:
            raise HTTPException(status_code=404, detail="Spec content not found in the external API response.")
        return spec_content
    except httpx.HTTPStatusError as exc:
        raise HTTPException(
            status_code=exc.response.status_code,
            detail={
                "message": f"specs/{spec_id} endpoint returned an error",
                "response": exc.response.json(),
            }
        )
