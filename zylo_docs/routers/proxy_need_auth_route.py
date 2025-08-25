from fastapi import APIRouter, Request, Response, Depends, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
import json
import httpx
from io import BytesIO
from pydantic import BaseModel, Field
from enum import Enum
from fastapi.responses import JSONResponse
from zylo_docs.services.openapi_service import OpenApiService
from zylo_docs.services.hub_server_service import get_spec_content_by_id
from zylo_docs.services.user_server_service import get_cur_test_case, update_current_spec
from zylo_docs.security import verify_token
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



@router.post("/zylo-ai", include_in_schema=False)
async def create_zylo_ai(request: Request, body: ZyloAIRequestBody, credentials: HTTPAuthorizationCredentials = Depends(verify_token)):
    access_token = credentials.credentials
    service: OpenApiService = request.app.state.openapi_service
    openapi_dict = service.get_current_spec()

    openapi_json_content = json.dumps(openapi_dict, indent=2).encode('utf-8')
    openapi_file_like = BytesIO(openapi_json_content)
    # timeout 버그를 피하기 위해 timeout을 None으로 설정
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
        try:
            tuned_spec_content = await get_spec_content_by_id(spec_id, client, access_token)
            service.set_current_spec(tuned_spec_content)
            return JSONResponse(
                content={
                    "success": True,
                    "message": f"Successfully tuned and applied spec_id: {spec_id}",
                }
            )
        
        except httpx.HTTPStatusError as exc:
            return JSONResponse(
                status_code=exc.response.status_code,
                content={
                    "success": False,
                    "message": "Failed to retrieve tuned spec content",
                    "details": f"specs/{spec_id} endpoint returned an error",
                }
            )

@router.post("/zylo-ai/user-context", include_in_schema=False)
async def create_zylo_ai_user_context(request: Request, body: ZyloAIUserContextRequestBody, credentials: HTTPAuthorizationCredentials = Depends(verify_token)):
    access_token = credentials.credentials
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
            "base_spec_id": body.spec_id,
            "user_context": body.user_context
        }
        try:
            resp = await client.post(
                f"{EXTERNAL_API_BASE}/zylo-ai/user-context", 
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
        try:
            tuned_spec_content = await get_spec_content_by_id(spec_id, client, access_token)
            service.set_current_spec(tuned_spec_content)
            return JSONResponse(
                content={
                    "success": True,
                    "message": f"Successfully tuned and applied spec_id: {spec_id}",
                }
            )
        
        except httpx.HTTPStatusError as exc:
            return JSONResponse(
                status_code=exc.response.status_code,
                content={
                    "success": False,
                    "message": "Failed to retrieve tuned spec content",
                    "details": f"specs/{spec_id} endpoint returned an error",
                }
            )
        
@router.get("/specs/me",include_in_schema=False)
async def get_spec(credentials: HTTPAuthorizationCredentials = Depends(verify_token)):
    access_token = credentials.credentials
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(f"{EXTERNAL_API_BASE}/specs/me", headers={"Authorization": f"Bearer {access_token}"})
            resp.raise_for_status()
            return resp.json()
        except httpx.HTTPStatusError as exc:
            return Response(
                content=exc.response.content,
                status_code=exc.response.status_code,
                media_type=exc.response.headers.get("content-type")
            )
        
        
    return Response(
        content=resp.content,
        media_type=resp.headers.get("content-type")
    )

@router.post("/toggle/spec/{spec_id}", include_in_schema=False)
async def get_specs_me_by_id(request: Request, spec_id: str, source: str = Query(...), credentials: HTTPAuthorizationCredentials = Depends(verify_token)):
    access_token = credentials.credentials
    async with httpx.AsyncClient() as client:
        try:
            spec_content = await get_spec_content_by_id(spec_id, client, access_token, source=source)
            service: OpenApiService = request.app.state.openapi_service
            service.set_current_spec(spec_content)
            return JSONResponse(
                    content={
                        "success": True,
                        "message": "Spec retrieved successfully",
                    }
                )
        except httpx.HTTPStatusError as exc:
            return Response(
                content=exc.response.content,
                status_code=exc.response.status_code,
                media_type=exc.response.headers.get("content-type")
            )

@router.patch("/testcases", include_in_schema=False)
async def create_test_case(request: Request, body: TestCasePatchBody, credentials: HTTPAuthorizationCredentials = Depends(verify_token)):
    access_token = credentials.credentials
    spec_id, path, method = body.spec_id, body.path, body.method.lower()
    cur_test_case = await get_cur_test_case(request, path, method)
    request_data = {"spec_data": cur_test_case, "spec_id": spec_id} 
    timeout = httpx.Timeout(timeout=None, connect=None, read=None, write=None)
    async with httpx.AsyncClient(timeout=timeout) as client:
        try:
            resp = await client.post(f"{EXTERNAL_API_BASE}/zylo-ai/testcases", json=request_data, headers={"Authorization": f"Bearer {access_token}"})
            resp.raise_for_status()
            await update_current_spec(request, resp.json().get("data", {}).get("tuned_json",{}), path, method)
            return resp.json()
        except httpx.HTTPStatusError as exc:
            return Response(
                content=exc.response.content,
                status_code=exc.response.status_code,
                media_type=exc.response.headers.get("content-type")
            )


@router.post("/pivot-current-spec/{spec_id}", include_in_schema=False)
async def get_spec_by_id(request: Request, spec_id: str, credentials: HTTPAuthorizationCredentials = Depends(verify_token)):
    access_token = credentials.credentials
    if spec_id == "original":
        service: OpenApiService = request.app.state.openapi_service
        service.set_current_spec(request.app.openapi())
        return JSONResponse(
            content={
                "success": True,
                "message": "Original OpenAPI spec retrieved successfully",
            }
        )
    else:
        async with httpx.AsyncClient() as client:
            try:
                spec_content = await get_spec_content_by_id(spec_id, client, access_token)
                service: OpenApiService = request.app.state.openapi_service
                service.set_current_spec(spec_content)
                return JSONResponse(
                    content={
                        "success": True,
                        "message": "Spec retrieved successfully",
                    }
                )
            except httpx.HTTPStatusError as exc:
                return JSONResponse(
                    status_code=exc.response.status_code,
                    content={
                        "success": False,
                        "message": "Failed to retrieve spec content",
                        "details": f"specs/{spec_id} endpoint returned an error",
                    }
                )
            

    
@router.post("/projects/{dummy_id}/specs/{spec_id}/invite", include_in_schema=False)
async def get_project_members(dummy_id: str, spec_id: str, body: InviteRequestBody , credentials: HTTPAuthorizationCredentials = Depends(verify_token)):
    access_token = credentials.credentials
    project_id = ""
    emails = body.emails
    timeout = httpx.Timeout(timeout=None, connect=None, read=None, write=None)
    async with httpx.AsyncClient(timeout=timeout) as client:
        try:
            resp = await client.get(f"{EXTERNAL_API_BASE}/projects", headers={"Authorization": f"Bearer {access_token}"})
            resp.raise_for_status()
            project_list = resp.json().get("data", [])
            if not project_list:
                return JSONResponse(
                    status_code=400,
                    content={
                        "success": False,
                        "message": "Since the user has never run zylo-ai, the project hasn’t been created yet.",
                        "error": {
                            "code": "PROJECT_NOT_FOUND",
                            "details": "Please run zylo-ai first to create a project and then try again."
                        }
                    }
                )
            # 지금은 아이디 하나당 하나의 프로젝트만 있다고 가정하기 때문에 인덱스0에서 Project_id를 가져옴
            project_id = project_list[0].get("project_id")
        
        except httpx.HTTPStatusError as exc:
            logger.warning(f"HTTP error during project fetch: {exc}")
            return JSONResponse(
                status_code=exc.response.status_code,
                content={
                    "success": False,
                    "message": "Failed to fetch project list.",
                    "error": {
                        "code": "EXTERNAL_API_ERROR",
                        "details": exc.response.text
                    }
                }
            )

    async with httpx.AsyncClient(timeout=timeout) as client:
        resp = await client.post(
            f"{EXTERNAL_API_BASE}/projects/{project_id}/specs/{spec_id}/invite",
            headers={"Authorization": f"Bearer {access_token}"},
            json={"emails": emails}
        )
        resp.raise_for_status()
        return JSONResponse(status_code=200, content=resp.json())


