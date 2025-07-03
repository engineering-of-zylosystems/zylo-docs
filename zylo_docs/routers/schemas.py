from fastapi import APIRouter, HTTPException
from zylo_docs.services.user_server_service import get_user_schemas
from zylo_docs.schemas.schema_data import SchemaResponseModel, SchemaData # SchemaData는 여기서는 직접 사용되지 않지만, import 자체는 문제 없음

router = APIRouter()
@router.get("/",response_model=SchemaResponseModel)
async def get_schemas():

    result = await get_user_schemas()
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