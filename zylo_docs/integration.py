import os
from fastapi import FastAPI,Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from .routers import front_route, proxy_route, proxy_need_auth_route
from .middlewares.exception_handler import ExceptionHandlingMiddleware
from zylo_docs.services.openapi_service import OpenApiService 
from zylo_docs.logging import NoZyloDocsLogFilter
from dotenv import load_dotenv

# config.py 파일의 위치를 기준으로 상위 폴더의 .env 파일을 찾습니다.
dotenv_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(dotenv_path=dotenv_path)
# 로깅 삭제하는 코드 개발 모드에서는 주석 처리
if os.getenv("DEV") != "dev":
    NoZyloDocsLogFilter().setup_logging()
HOST = os.getenv("SERVER_HOST", "localhost")
PORT = os.getenv("SERVER_PORT", "8000")

def set_initial_openapi_spec(app: FastAPI):
    openapi_json = app.openapi()
    app.state.openapi_service.set_current_spec(openapi_json)

    message = f"""
┌───────────────────────────────────────────────────────────────────────────┐
│                                                                           │
│  🚀 zylo-docs is running locally!                                         │
│                                                                           │
│  🔗 http://{HOST}:{PORT}/zylo-docs                                       │
│                                                                           │
│  Check your API spec using the zylo-docs web app.                         │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────┘
"""
    print(message)

def zylo_docs(app: FastAPI):
    @app.on_event("startup")
    async def on_startup():
        set_initial_openapi_spec(app)
    if not hasattr(app.state, 'openapi_service'):
        app.state.openapi_service = OpenApiService()
        
    app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "static")), name="static")

    app.include_router(front_route.router, prefix="/zylo-docs", tags=["front"])
    app.include_router(proxy_need_auth_route.router, prefix="/zylo-docs/api", tags=["proxy_auth"])
    app.include_router(proxy_route.router, prefix="/zylo-docs/api", tags=["proxy"])
    app.add_middleware(ExceptionHandlingMiddleware)

    @app.get("/zylo-docs{full_path:path}", include_in_schema=False)
    async def serve_react_app():
        return FileResponse(os.path.join(os.path.dirname(__file__), "static", "index.html"))
