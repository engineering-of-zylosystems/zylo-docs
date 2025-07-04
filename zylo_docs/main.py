import os
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from zylo_docs.schemas.response import APIErrorDetail, APIErrorResponse, APIResponse
from zylo_docs.routers import schemas
from zylo_docs.exceptions import APIException


app = FastAPI(title="Zylo Docs API")


app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "static")), name="static")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/health")
def health_check():
    return APIResponse(
        success=True,
        message="Zylo-hub-be API server is running.",
        data=None
    )

app.include_router(schemas.router, prefix="/schemas", tags=["schemas"])

# 모든 경로에 대해 정적 프론트 서빙
@app.get("/")
async def serve_react_app():
    print(f"Serving React app")
    return FileResponse(os.path.join(os.path.dirname(__file__), "static", "index.html"))

@app.exception_handler(APIException)
async def api_exception_handler(request: Request, exc: APIException):
    return JSONResponse(
        status_code=exc.status_code,
        content=APIErrorResponse(
            success=False,
            message=exc.message,
            data=APIErrorDetail(
                code=exc.error.code,
                details=exc.error.details
            )
        ).model_dump()
    )
