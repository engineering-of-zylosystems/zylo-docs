from fastapi import APIRouter,Query, Request,HTTPException
from zylo_docs.services.user_server_service import get_user_operation,get_user_operation_by_path
from zylo_docs.schemas.schema_data import SchemaResponseModel
from zylo_docs.schemas.schema_data import APIRequestModel
from zylo_docs.services.openapi_service import OpenApiService
from fastapi.responses import JSONResponse
from zylo_docs.utils.error_response import make_error_response
import urllib.parse
import httpx

router = APIRouter()
@router.get("/openapi.json", include_in_schema=False)
async def get_openapi_json(request: Request):
    openapi = request.app.openapi()
    return{
        "success": True,
        "message": "OpenAPI JSON retrieved successfully",
        "data":openapi
    }
# @router.get("/operation", response_model=SchemaResponseModel, include_in_schema=False)
# async def get_operation(request: Request):
#     try:
#         result = await get_user_operation(request)
#         if not result["operationGroups"]:
#             raise HTTPException(
#                 status_code=404,
#                 detail={
#                     "success": False,
#                     "message": "Operation not found",
#                     "data": {
#                         "code": "OPERATION_NOT_FOUND",
#                         "details": "No operation found with operationId 'invalidId'"
#                     }
#                 }
#             )

#         return {
#             "success": True,
#             "message": "All operation listed",
#             "data": result
#         }
#     except Exception as e:
#         raise ValueError(f"Unexpected error: {e}")

@router.get("/operation/by-path", include_in_schema=False)
async def get_operation_by_path(
    request: Request,
    path: str = Query(..., description="조회할 operationId"),
    method: str = Query(..., description="HTTP 메소드")
):
    result = await get_user_operation_by_path(request, path, method)
    if not result or not result.get(method):
        raise HTTPException(
            status_code=404,
            detail={
                "success": False,
                "message": "Operation not found",
                "data": {
                    "code": "OPERATION_NOT_FOUND",
                    "details": f"No operation found with operationId '{path}'"
                }
            }
        )
    return {
        "success": True,
        "message": "Operation retrieved successfully",
        "data": result.get(method)
    }
@router.get("/current-spec", include_in_schema=False)
async def get_current_spec(request: Request):
    service: OpenApiService = request.app.state.openapi_service
    openapi_json = service.get_current_spec()
    return {
        "success": True,
        "message": "Current OpenAPI spec retrieved successfully",
        "data": openapi_json
    }


@router.post("/test-execution", include_in_schema=False)
async def test_execution(request: Request, request_data: APIRequestModel):
    target_path = request_data.path

    # 헤더 파싱
    request_headers = {k: str(v) for k, v in (request_data.input.headers or {}).items()} if request_data.input else {}

    # 쿠키 처리
    if request_data.input and getattr(request_data.input, "cookie_params", None):
        if request_data.input.cookie_params is not None:
            cookie_header = "; ".join(f"{k}={v}" for k, v in request_data.input.cookie_params.items())
            request_headers["Cookie"] = cookie_header

    target_path = request_data.path
    if request_data.input and request_data.input.path_params:
        for k, v in request_data.input.path_params.items():
            target_path = target_path.replace(f"{{{k}}}", str(v))
    target_path = urllib.parse.urljoin(str(request.base_url), target_path)

    target_path = urllib.parse.urljoin(str(request.base_url), target_path)
    # 자기 자신의 api 호출
    transport = httpx.ASGITransport(app=request.app)
    async with httpx.AsyncClient(transport=transport) as client:
        try:
            response = await client.request(
                method=request_data.method,
                url=target_path,
                params=request_data.input.query_params if request_data.input else None,
                json=request_data.input.body.value if request_data.input else None,
                headers=request_headers
            )

            # 프록시된 응답에서 헤더를 복사하되, Content-Length 및 Transfer-Encoding은 제외합니다.
            # 이는 JSONResponse가 새 본문에 대해 올바른 길이를 계산하도록 하기 위함입니다.
            proxied_headers = dict(response.headers)
            if "content-length" in proxied_headers:
                del proxied_headers["content-length"]
            if "transfer-encoding" in proxied_headers:
                del proxied_headers["transfer-encoding"]

            # 대상 백엔드에서 에러를 반환했을 경우
            if response.is_client_error or response.is_server_error:
                # 콘텐츠를 JSON으로 파싱 시도, JSON이 아니면 텍스트로 폴백
                try:
                    error_content = response.json()
                except ValueError:
                    error_content = response.text

                return JSONResponse(
                    status_code=response.status_code,
                    content={
                        "success": False,
                        "message": f"An error was returned from the user backend ({response.status_code})",
                        "data": {
                            "code": f"TARGET_BACKEND_ERROR_{response.status_code}",
                            "details": error_content
                        }
                    },
                    headers=proxied_headers, # 수정된 헤더 사용
                    media_type=response.headers.get("content-type", "application/json")
                )

            # 테스트가 성공했을 경우 json 또는 text 응답 반환
            try:
                success_content = response.json()
            except ValueError:
                success_content = response.text

            return JSONResponse(
                status_code=response.status_code,
                content={
                    "success": response.is_success,
                    "message": "test case success." if response.is_success else "test case fail.",
                    "data": success_content,
                },
                headers={k: v for k, v in response.headers.items() if k.lower() not in ["content-length", "transfer-encoding"]},
                media_type=response.headers.get("content-type", "application/json"),
            )

        except httpx.RequestError as e:
            return make_error_response(500, "HTTPX_REQUEST_ERROR", "네트워크/연결 오류", str(e))
        except Exception as e:
            return make_error_response(500, "UNEXPECTED_PROXY_ERROR", "프록시 실행 중 예상치 못한 오류", str(e))
