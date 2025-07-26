from fastapi import APIRouter,Query, Request,HTTPException
from fastapi.responses import Response
from zylo_docs.services.openapi_service import OpenApiService
from zylo_docs.services.user_server_service import get_user_operation,get_user_operation_by_path
from zylo_docs.schemas.schema_data import SchemaResponseModel
from zylo_docs.schemas.schema_data import APIRequestModel
from fastapi.responses import JSONResponse
import urllib.parse
import httpx

router = APIRouter()
@router.get("/operation", response_model=SchemaResponseModel, include_in_schema=False)
async def get_operation(request: Request):
    try:
        result = await get_user_operation(request)
        if not result["operationGroups"]:
            raise HTTPException(
                status_code=404,
                detail={
                    "success": False,
                    "message": "Operation not found",
                    "data": {
                        "code": "OPERATION_NOT_FOUND",
                        "details": "No operation found with operationId 'invalidId'"
                    }
                }
            )

        return {
            "success": True,
            "message": "All operation listed",
            "data": result
        }
    except Exception as e:
        raise ValueError(f"Unexpected error: {e}")

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

@router.post("/test-execution", include_in_schema=False)
async def test_execution(request: Request, request_data: APIRequestModel):
    target_path = request_data.path
    if request_data.input and request_data.input.path_params:
        for key, value in request_data.input.path_params.items():
            placeholder = f"{{{key}}}"
            target_path = target_path.replace(placeholder, str(value))
    # 자신의 서버로 경로 변경 
    target_path = urllib.parse.urljoin(str(request.base_url), target_path)
    # 별도의 HTTP 서버를 실행할 필요 없이 FastAPI 애플리케이션 인스턴스로 직접 요청을 보내기 위해
    # ASGITransport를 사용합니다.
    transport = httpx.ASGITransport(app=request.app)
    async with httpx.AsyncClient(transport=transport) as client:
        try:

            response = await client.request(
                method=request_data.method,
                url=target_path,
                params=request_data.input.query_params if request_data.input else None,
                json=request_data.input.body.value if request_data.input else None
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
                    "success": True,
                    "message": "요청이 성공적으로 처리되었습니다.",
                    "data": success_content # 대상 백엔드의 실제 응답 데이터
                },
                headers=proxied_headers, # 수정된 헤더 사용
                media_type=response.headers.get("content-type", "application/json")
            )

        except httpx.RequestError as e:
            # 이는 httpx의 네트워크 관련 오류(예: 연결 거부, 타임아웃, DNS 오류)를 잡습니다.
            # 요청 실패에 대한 HTTPError보다 더 구체적인 예외 처리입니다.
            return JSONResponse(
                status_code=500,
                content={
                    "success": False,
                    "message": "대상 백엔드로의 요청이 실패했습니다 (네트워크/연결 오류)",
                    "data": {
                        "code": "HTTPX_REQUEST_ERROR",
                        "details": str(e)
                    }
                }
            )
        except httpx.HTTPStatusError as e:
            return JSONResponse(
                status_code=e.response.status_code if e.response else 500,
                content={
                    "success": False,
                    "message": "대상 백엔드에서 HTTP 상태 오류가 반환되었습니다 (raise_for_status를 통해)",
                    "data": {
                        "code": f"HTTPX_STATUS_ERROR_{e.response.status_code if e.response else 'UNKNOWN'}",
                        "details": str(e),
                        "response_content": e.response.text if e.response else None
                    }
                }
            )
        except Exception as e:
            # 이는 이 프록시 함수 실행 중에 발생할 수 있는 다른 예상치 못한 오류를 위한
            return JSONResponse(
                status_code=500,
                content={
                    "success": False,
                    "message": "프록시 실행 중 예상치 못한 오류가 발생했습니다.",
                    "data": {
                        "code": "UNEXPECTED_PROXY_ERROR",
                        "details": str(e)
                    }
                }
            )
