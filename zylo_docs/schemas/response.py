from typing import Any, Dict, Generic, TypeVar, Optional
from pydantic import BaseModel
from pydantic.generics import GenericModel

T = TypeVar("T")
class APIResponse(GenericModel, Generic[T]):
    success: bool = True
    message: str
    data: Optional[T] = None

class APIErrorDetail(BaseModel):
    code: str
    details: Optional[Any] = None  # 또는 Dict[str, Any]도 가능

class APIErrorResponse(BaseModel):
    success: bool = False
    message: str
    data: APIErrorDetail

