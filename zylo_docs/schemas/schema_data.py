from pydantic import BaseModel, Field
from typing import Any, Dict, Optional

class SchemaResponseModel(BaseModel):
    success: bool
    message: str
    data: Any
class APIResponseBodyModel(BaseModel):
    value: Optional[Dict[str, Any]] = Field(default_factory=dict)

class APIInputModel(BaseModel):
    path_params: Optional[Dict[str, Any]] = Field(default_factory=dict)
    query_params: Optional[Dict[str, Any]] = Field(default_factory=dict)
    cookie_params: Optional[Dict[str, Any]] = Field(default_factory=dict)
    headers: Optional[Dict[str, Any]] = Field(default_factory=dict)
    body: APIResponseBodyModel = Field(default_factory=APIResponseBodyModel)
class APIRequestModel(BaseModel):
    method: str
    path: str
    input: APIInputModel = Field(default_factory=APIInputModel)

