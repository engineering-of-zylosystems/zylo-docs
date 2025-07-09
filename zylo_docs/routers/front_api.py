from fastapi import APIRouter,Query, Request,HTTPException
from zylo_docs.services.user_server_service import get_user_schemas, get_user_operation,get_user_operation_by_id
from zylo_docs.schemas.schema_data import SchemaResponseModel
from zylo_docs.schemas.schema_data import APIRequestModel
from fastapi.responses import JSONResponse
import httpx

router = APIRouter()
@router.get("/schemas",response_model=SchemaResponseModel, include_in_schema=False)
async def get_schemas(request: Request):
    try:
        result = await get_user_schemas(request)
        if result is None or not result: 
            raise HTTPException(
                status_code=404,
                detail={
                    "success": False,
                    "message": "Schemas are not found in localmachine ",
                    "error": {
                    "code": "SCHEMAS_NOT_FOUND",
                    "details": "No schemas found with all_schemas.json"
                    }
                }
            )
        return {
            "success": True,
            "message": "All schemas retrieved successfully",
            "data":{
                "details": result
            }
        }
    except:
        raise ValueError("Invalid operationId 'invalidId'")
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

@router.get("/operation/by-id", include_in_schema=False)
async def get_operation_by_id(
    request: Request,
    url: str = Query(..., description="조회할 operationId (예: /auth/login)"),
    method: str = Query(..., description="HTTP 메소드 (예: GET, POST 등)")
):
    result = await get_user_operation_by_id(request, url, method)
    if not result:
        raise HTTPException(
            status_code=404,
            detail={
                "success": False,
                "message": "Operation not found",
                "data": {
                    "code": "OPERATION_NOT_FOUND",
                    "details": f"No operation found with operationId '{url}'"
                }
            }
        )
    return {
        "success": True,
        "message": "Operation retrieved successfully",
        "data": result
    }

@router.post("/test-executions", include_in_schema=False)
async def test_executions(request: Request, request_data: APIRequestModel):

    target_path = request_data.path
    if request_data.path_params:
        for key, value in request_data.path_params.items():
            placeholder = f":{key}"
            target_path = target_path.replace(placeholder, str(value))
    transport = httpx.ASGITransport(app=request.app)

    async with httpx.AsyncClient(transport=transport, base_url="http://") as client:
        response = await client.request(
            method=request_data.method,
            url=target_path,
            params=request_data.query_params,
            json=request_data.body
        )
        if 200 <= response.status_code < 300:
            return {
                "success": True,
                "message": "Request executed successfully",
                "data": response.json() if response.content else None
            }
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "message": "Test failed",
                "code": "INTERNAL_LOGIC_TEST_FAILED",
                "data": response.json() if response.content else None
            }
        )
