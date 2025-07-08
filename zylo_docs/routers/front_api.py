from fastapi import APIRouter,Query, Request,HTTPException
from zylo_docs.services.user_server_service import get_user_schemas, get_user_operation,get_user_operation_by_id
from zylo_docs.schemas.schema_data import SchemaResponseModel

router = APIRouter()
@router.get("/schemas",response_model=SchemaResponseModel, include_in_schema=False)
async def get_schemas(request: Request):
    try:
        result = await get_user_schemas(request)
        if result is None or not result: # None이거나 빈 리스트일 때 404 처리 (스키마가 없는 것도 자원 없음으로 간주)
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
    print(result)
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
