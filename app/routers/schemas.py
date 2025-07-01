from fastapi import APIRouter
from app.services.user_server_service import get_user_schemas
from app.schemas.schema_data import SchemaResponseModel

router = APIRouter()
@router.get("/", response_model= SchemaResponseModel)
async def get_schemas():
    print("Fetching schemas from user server...")
    result = await get_user_schemas()
    return {
        "message": "All schemas retrieved successfully",
        "data": result
    }