from pydantic import BaseModel, Field
from typing import Any, Dict, Optional

class SchemaResponseModel(BaseModel):
    success: bool
    message: str
    data: Any
class APIInputModel(BaseModel):
    path: Optional[Dict[str, Any]] = Field(default_factory=dict)
    query: Optional[Dict[str, Any]] = Field(default_factory=dict)
    body: Optional[Dict[str, Any]] = Field(default_factory=dict)
class APIRequestModel(BaseModel):
    method: str
    path: str
    input: APIInputModel = Field(default_factory=APIInputModel)

