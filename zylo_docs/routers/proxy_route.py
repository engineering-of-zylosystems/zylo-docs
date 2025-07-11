from fastapi import APIRouter, Request
from fastapi import Request, Response
from typing import Optional
import json
import httpx
from io import BytesIO
from pydantic import BaseModel, Field
from enum import Enum
EXTERNAL_API_BASE = "https://api.zylosystems.com"
router = APIRouter()
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
    openapi_dict = request.app.openapi()
    openapi_json_content = json.dumps(openapi_dict, indent=2).encode('utf-8')
    openapi_file_like = BytesIO(openapi_json_content)
    timeout = httpx.Timeout(60.0, connect=5.0)
    async with httpx.AsyncClient(timeout=timeout) as client:
        # 1. 파일 데이터는 'files' 파라미터용으로 분리합니다.
        files_for_upload = {
            'file': ('openapi.json', openapi_file_like, 'application/json')
        }

        # 2. 텍스트 데이터는 'data' 파라미터용으로 분리합니다.
        text_data = {
            "title": body.title,
            "version": body.version,
            "doc_type": body.doc_type.value,
        }

        # 테스트를 위해 임시로 access_token을 하드코딩
        access_token = "eyJhbGciOiJIUzI1NiIsImtpZCI6IldsSEd6eVR0emtaaC9GOVAiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL21hdXhmc3NjZnpvcmlqdGdubWplLnN1cGFiYXNlLmNvL2F1dGgvdjEiLCJzdWIiOiJkYTAwMWEyYi1iMjg1LTRiOGUtYTZmMi0xN2M4MjhiZDQ3ZWEiLCJhdWQiOiJhdXRoZW50aWNhdGVkIiwiZXhwIjoxNzUyMjI1OTA3LCJpYXQiOjE3NTIyMjIzMDcsImVtYWlsIjoic2VvYWtAenlsb3N5c3RlbXMuY29tIiwicGhvbmUiOiIiLCJhcHBfbWV0YWRhdGEiOnsicHJvdmlkZXIiOiJlbWFpbCIsInByb3ZpZGVycyI6WyJlbWFpbCJdfSwidXNlcl9tZXRhZGF0YSI6eyJlbWFpbCI6InNlb2FrQHp5bG9zeXN0ZW1zLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJwaG9uZV92ZXJpZmllZCI6ZmFsc2UsInN1YiI6ImRhMDAxYTJiLWIyODUtNGI4ZS1hNmYyLTE3YzgyOGJkNDdlYSJ9LCJyb2xlIjoiYXV0aGVudGljYXRlZCIsImFhbCI6ImFhbDEiLCJhbXIiOlt7Im1ldGhvZCI6InBhc3N3b3JkIiwidGltZXN0YW1wIjoxNzUyMjIyMzA3fV0sInNlc3Npb25faWQiOiI5Njk0OTAwZC02NWVjLTRiMmUtYjQwOS04YjJmMmY0MTZlNzciLCJpc19hbm9ueW1vdXMiOmZhbHNlfQ.Q-Eeo3VUl9AxfCzhBSCEq5CuIOcbL7An5wVCqmxeVvM"
        
        # 3. client.post 호출 시 'files'와 'data'를 구분하여 전달합니다.
        resp = await client.post(
            f"{EXTERNAL_API_BASE}/zylo-ai", 
            files=files_for_upload, 
            data=text_data,
            headers={
                "Authorization": f"Bearer {access_token}"
            }
        )
        print(f"Response status code: {resp.status_code}")
    return Response(
        content=resp.content,
        media_type=resp.headers.get("content-type")
    )

@router.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"], include_in_schema=False)
async def proxy(request: Request, path: str):
        async with httpx.AsyncClient() as client:
            proxy_url = f"{EXTERNAL_API_BASE}/{path}"
            body = await request.body()
            headers = dict(request.headers)
            headers.pop("host", None)  # host 헤더 제거 제거해야 안점함

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

