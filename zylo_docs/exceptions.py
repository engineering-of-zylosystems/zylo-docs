from typing import Optional, Dict, Any

from zylo_docs.schemas.response import APIErrorDetail

class APIException(Exception):
    def __init__(
        self, 
        message: str, 
        code: str = "UNKNOWN_ERROR", 
        status_code:int = 400,
        error: Optional[Dict[str, Any]] = None,
        success: bool = False
    ):
        self.status_code = status_code
        self.message = message
        self.error = APIErrorDetail(code=code, details=error) if error is None else error
        self.success = success

