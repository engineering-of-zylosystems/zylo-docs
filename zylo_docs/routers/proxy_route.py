import pprint
from fastapi import APIRouter, Request
from fastapi import Request, Response
from typing import Optional
import json
import httpx
from io import BytesIO
from pydantic import BaseModel, Field
from enum import Enum
from zylo_docs.services.openapi_service import openapi_service
from fastapi.responses import JSONResponse

EXTERNAL_API_BASE = "https://api.zylosystems.com"
router = APIRouter()
# 테스트를 위해 임시로 access_token을 하드코딩
access_token = "eyJhbGciOiJIUzI1NiIsImtpZCI6IldsSEd6eVR0emtaaC9GOVAiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL21hdXhmc3NjZnpvcmlqdGdubWplLnN1cGFiYXNlLmNvL2F1dGgvdjEiLCJzdWIiOiJkYTAwMWEyYi1iMjg1LTRiOGUtYTZmMi0xN2M4MjhiZDQ3ZWEiLCJhdWQiOiJhdXRoZW50aWNhdGVkIiwiZXhwIjoxNzUzMDc1ODEwLCJpYXQiOjE3NTI0NzEwMTAsImVtYWlsIjoic2VvYWtAenlsb3N5c3RlbXMuY29tIiwicGhvbmUiOiIiLCJhcHBfbWV0YWRhdGEiOnsicHJvdmlkZXIiOiJlbWFpbCIsInByb3ZpZGVycyI6WyJlbWFpbCJdfSwidXNlcl9tZXRhZGF0YSI6eyJlbWFpbCI6InNlb2FrQHp5bG9zeXN0ZW1zLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJwaG9uZV92ZXJpZmllZCI6ZmFsc2UsInN1YiI6ImRhMDAxYTJiLWIyODUtNGI4ZS1hNmYyLTE3YzgyOGJkNDdlYSJ9LCJyb2xlIjoiYXV0aGVudGljYXRlZCIsImFhbCI6ImFhbDEiLCJhbXIiOlt7Im1ldGhvZCI6InBhc3N3b3JkIiwidGltZXN0YW1wIjoxNzUyNDcxMDEwfV0sInNlc3Npb25faWQiOiI3YzliMjlmOC0wZmEzLTQ1MGMtOWJjYy0yMWQxZWFkNmY0M2IiLCJpc19hbm9ueW1vdXMiOmZhbHNlfQ._ISb5WTa8c7GBI8GKRjneCfaQZ47nROcUxoXgPUWwtc"

class DocTypeEnum(str, Enum):
    internal = "internal"
    public = "public"
    partner = "partner"

class ZyloAIRequestBody(BaseModel):
    title: str = Field(..., description="Title of the OpenAPI spec")
    version: str = Field(..., description="Version of the spec")
    doc_type: DocTypeEnum

@router.post("/zylo-ai", include_in_schema=False)
async def create_zylo_ai(request: Request, body: ZyloAIRequestBody):
    service: OpenApiService = request.app.state.openapi_service
    openapi_dict = service.get_current_spec()
    openapi_json_content = json.dumps(openapi_dict, indent=2).encode('utf-8')
    openapi_file_like = BytesIO(openapi_json_content)
    timeout = httpx.Timeout(timeout=None, connect=None, read=None, write=None)
    async with httpx.AsyncClient(timeout=timeout) as client:
        files_for_upload = {
            'file': ('openapi.json', openapi_file_like, 'application/json')
        }
        text_data = {
            "title": body.title,
            "version": body.version,
            "doc_type": body.doc_type.value,
        }
        try:
            resp = await client.post(
                f"{EXTERNAL_API_BASE}/zylo-ai", 
                files=files_for_upload, 
                data=text_data,
                headers={
                    "Authorization": f"Bearer {access_token}"
                }
            )
            resp.raise_for_status()
        
        except httpx.HTTPStatusError as exc:
            return Response(
                content=exc.response.content,
                status_code=exc.response.status_code,
                media_type=exc.response.headers.get("content-type")
            )
        
        response_json = resp.json()

        spec_id = response_json.get("data", {}).get("id")
        if not spec_id:
            return Response(content="Response JSON does not contain 'data.id' field.",status_code=400)
        query_params = {"spec_id": "tuned"}
        ai_hub_api = f"{EXTERNAL_API_BASE}/specs/{spec_id}"
        ai_hub_json = await client.get(ai_hub_api, params=query_params,  headers={
                "Authorization": f"Bearer {access_token}"
            })
        openapi_service.set_latest(ai_hub_json.json())


    return Response(
        content=ai_hub_json.content,
        media_type=ai_hub_json.headers.get("content-type")
    )


@router.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"], include_in_schema=False)
async def proxy(request: Request, path: str):
    if path == 'zylo-ai' and request.method == 'POST':
        try:
            body = ZyloAIRequestBody(**await request.json())
            return await create_zylo_ai(body)
        except json.JSONDecodeError:
            return JSONResponse(status_code=400, content={"message": "Invalid JSON body"})
        except Exception as e:
            return JSONResponse(status_code=400, content={"message": f"Invalid request body: {e}"})

    async with httpx.AsyncClient() as client:
        proxy_url = f"{EXTERNAL_API_BASE}/{path}"
        body = await request.body()
        headers = dict(request.headers)
        headers.pop("host", None)

        resp = await client.request(
            method=request.method,
            url=proxy_url,
            content=body,
            headers=headers,
            params=request.query_params,
        )
    headers_to_frontend = dict(resp.headers)
    # 프론트로 보내는 응답 객체 프론트와 인터페이스를 맞춰야함
    return Response(
        headers=headers_to_frontend,
        content=resp.content,
        media_type=resp.headers.get("content-type")
    )

