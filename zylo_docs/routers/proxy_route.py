from fastapi import APIRouter, Request,Response, Query
from typing import Optional
import httpx
from pydantic import BaseModel, Field
from enum import Enum
from zylo_docs.services.openapi_service import OpenApiService
from zylo_docs.config import EXTERNAL_API_BASE
from pydantic import BaseModel
import logging
logger = logging.getLogger(__name__)

router = APIRouter()
class DocTypeEnum(str, Enum):
    internal = "internal"
    public = "public"
    partner = "partner"

class ZyloAIRequestBody(BaseModel):
    title: str = Field(..., description="Title of the OpenAPI spec")
    version: str = Field(..., description="Version of the spec")
    doc_type: DocTypeEnum
    
class ZyloAIUserContextRequestBody(BaseModel):
    title: str = Field(..., description="Title of the OpenAPI spec")
    version: str = Field(..., description="Version of the spec")
    doc_type: DocTypeEnum
    spec_id: str = Field(..., description="Spec ID for current spec")
    user_context: Optional[str] = Field(None, description="User context for the spec")
    
class InviteRequestBody(BaseModel):
    emails: list[str] = Field(..., description="List of emails to invite")
class TestCasePatchBody(BaseModel):
    spec_id: str = Field(..., description="Spec ID for the test case")
    path: str = Field(..., description="Operation ID for the test case")
    method: str = Field(..., description="Test case method")

            
@router.get("/download-spec", include_in_schema=False)
async def download_current_spec(request: Request, spec_id: str = Query(..., description="OpenAPI spec ID")):
    service: OpenApiService = request.app.state.openapi_service
    openapi_dict = service.get_current_spec()

    if spec_id == "original":
        return {
            "success": True,
            "message": "Original OpenAPI spec retrieved successfully",
            "data": request.app.openapi()
        }
    else:
        return {
                    "success": True,
                    "message": "Spec retrieved successfully",
                    "data": openapi_dict
                }
    
@router.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"], include_in_schema=False)
async def proxy(request: Request, path: str):
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
            status_code=resp.status_code,
            headers=headers_to_frontend,
            content=resp.content,
            media_type=resp.headers.get("content-type")
        )

