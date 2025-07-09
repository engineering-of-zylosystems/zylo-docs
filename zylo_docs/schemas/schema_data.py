from pydantic import BaseModel
from typing import Any, Dict, Optional

class SchemaResponseModel(BaseModel):
    success: bool
    message: str
    data: Any

class APIRequestModel(BaseModel):
    method: str
    operation: str
    path_params: Optional[Dict[str, Any]] = None
    query_params: Optional[Dict[str, Any]] = None
    body: Optional[Dict[str, Any]] = None