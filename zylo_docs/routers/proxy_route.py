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
access_token = "eyJhbGciOiJIUzI1NiIsImtpZCI6IldsSEd6eVR0emtaaC9GOVAiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL21hdXhmc3NjZnpvcmlqdGdubWplLnN1cGFiYXNlLmNvL2F1dGgvdjEiLCJzdWIiOiJkZTkwMDAwMS00OGRjLTQ1MzktYjEzNi1jYmQwNDdmMmE0ZDYiLCJhdWQiOiJhdXRoZW50aWNhdGVkIiwiZXhwIjoxNzUzMTUxNDA3LCJpYXQiOjE3NTI1NDY2MDcsImVtYWlsIjoiZHdkY3FkcUBuYXZlci5jb20iLCJwaG9uZSI6IiIsImFwcF9tZXRhZGF0YSI6eyJwcm92aWRlciI6ImVtYWlsIiwicHJvdmlkZXJzIjpbImVtYWlsIl19LCJ1c2VyX21ldGFkYXRhIjp7ImVtYWlsIjoiZHdkY3FkcUBuYXZlci5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwicGhvbmVfdmVyaWZpZWQiOmZhbHNlLCJzdWIiOiJkZTkwMDAwMS00OGRjLTQ1MzktYjEzNi1jYmQwNDdmMmE0ZDYifSwicm9sZSI6ImF1dGhlbnRpY2F0ZWQiLCJhYWwiOiJhYWwxIiwiYW1yIjpbeyJtZXRob2QiOiJwYXNzd29yZCIsInRpbWVzdGFtcCI6MTc1MjU0NjYwN31dLCJzZXNzaW9uX2lkIjoiNzc2NjBlYmUtYjYxMy00MjBkLTkxODgtYmMyMzhhZTFhN2ZlIiwiaXNfYW5vbnltb3VzIjpmYWxzZX0.ln_xGdmZunJ7VrPshnBAE3_YtdTYise_TxRUHFo7wn4"

class DocTypeEnum(str, Enum):
    internal = "internal"
    public = "public"
    partner = "partner"
class ZyloAIRequestBody(BaseModel):
    title: str = Field(..., description="Title of the OpenAPI spec")
    version: str = Field(..., description="Version of the spec")
    doc_type: DocTypeEnum
    
async def create_zylo_ai(request: Request):
    openapi_dict = openapi_service.get_latest()
    
    openapi_json_content = json.dumps(openapi_dict, indent=2).encode('utf-8')
    openapi_file_like = BytesIO(openapi_json_content)
    timeout = httpx.Timeout(60.0, connect=5.0)

    async with httpx.AsyncClient(timeout=timeout) as client:
        files_for_upload = {
            'file': ('openapi.json', openapi_file_like, 'application/json')
        }

        text_data = {
            "title": "title",
            "version": "version",
            "doc_type": "public"
        }

        resp = await client.post(
            f"{EXTERNAL_API_BASE}/zylo-ai", 
            files=files_for_upload, 
            data=text_data,
            headers={
                "Authorization": f"Bearer {access_token}"
            }
        )
        resp.raise_for_status()
        response_json = resp.json()

        spec_id = response_json.get("data", {}).get("id")
        if not spec_id:
            return Response(content="Response JSON does not contain 'data.id' field.",status_code=400)
        query_params = {"spec_id": "tuned"}
        ai_hub_api = f"{EXTERNAL_API_BASE}/specs/{spec_id}"
        ai_hub_response = await client.get(ai_hub_api, params=query_params,  headers={
                "Authorization": f"Bearer {access_token}"
            })
        ai_hub_response_json = ai_hub_response.json()
        tuned_api_json = ai_hub_response_json.get("data", {'spec_content':{}}).get('spec_content', {})
        openapi_service.set_latest(tuned_api_json)


    return JSONResponse(
        content=tuned_api_json
    )


@router.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"], include_in_schema=False)
async def proxy(request: Request, path: str):
    if path == 'zylo-ai' and request.method == 'POST':
        try:
            return await create_zylo_ai(request)
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
