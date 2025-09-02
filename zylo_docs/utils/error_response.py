from fastapi.responses import JSONResponse
from typing import Any
def make_error_response(status_code: int, code: str, message: str, details: Any = None):
    return JSONResponse(
        status_code=status_code,
        content={
            "success": False,
            "message": message,
            "data": {"code": code, "details": details},
        }
    )
