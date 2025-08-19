
from fastapi import Depends, HTTPException

from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer(auto_error=False)
async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):

    if credentials is None:
        # 토큰이 아예 없는 경우, 원하는 에러를 여기서 발생시킵니다.
        raise HTTPException(
            status_code=401,
            detail={
                "success": False,
                "message": "user's authorization is required, please sign in",
                "data": {
                    "code": "SIGN_IN_REQUIRED",
                    "details": "user's authorization is required."
                }
        }
    )
    access_token = credentials.credentials
    if not access_token:
        raise HTTPException(
                status_code=401,
                detail={
                    "success": False,
                    "message": "Invalid or missing access token",
                    "data": {
                        "code": "INVALID_ACCESS_TOKEN",
                        "details": "No operation found with operationId 'invalidId'"
                    }
                }
            )
    return credentials
