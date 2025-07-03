from pydantic import BaseModel
from typing import List, Dict, Any

SchemaMap = Dict[str, Any]  # 실제 schema json 구조 그대로 받을 경우

class SchemaData(BaseModel):
    details: List[SchemaMap]  # 각 schema의 상세 정보 리스트

class SchemaResponseModel(BaseModel):
    success: bool
    message: str
    data: SchemaData