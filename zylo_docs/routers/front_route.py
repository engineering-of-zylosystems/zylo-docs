from fastapi import APIRouter,Query, Request,HTTPException
from zylo_docs.services.openapi_service import OpenApiService
from zylo_docs.services.user_server_service import get_user_operation,get_user_operation_by_path
from zylo_docs.schemas.schema_data import SchemaResponseModel
from zylo_docs.schemas.schema_data import APIRequestModel
from fastapi.responses import JSONResponse
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

    target_operation = request_data.operation
    if request_data.path_params:
        for key, value in request_data.path_params.items():
            placeholder = f":{key}"
            target_operation = target_operation.replace(placeholder, str(value))
    transport = httpx.ASGITransport(app=request.app)

    async with httpx.AsyncClient(transport=transport) as client:
        try:
            response = await client.request(
                method=request_data.method,
                url=target_operation,
                params=request_data.query_params,
                json=request_data.body
            )
            if 200 <= response.status_code < 300:
                return JSONResponse(
                    status_code=200,
                    content={
                    "success": True,
                    "message": "Request executed successfully",
                    "data": response.json() if response.content else None
                })
            return JSONResponse(
                status_code=400,
                content={
                    "success": False,
                    "message": "Test failed",
                    "code": "INTERNAL_LOGIC_TEST_FAILED",
                    "data": response.json() if response.content else None
                }
            )
        except:
            return JSONResponse(
                status_code=400,
                content={
                    "success": False,
                    "message": "Test failed due to unexpected error",
                    "code": "UNEXPECTED_ERROR",
                    "data": None
                }
            )
