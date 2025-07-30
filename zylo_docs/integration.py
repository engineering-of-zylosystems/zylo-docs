import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from .routers import front_route, proxy_route 
from .middlewares.exception_handler import ExceptionHandlingMiddleware
from zylo_docs.services.openapi_service import OpenApiService 
from zylo_docs.logging import NoZyloDocsLogFilter
# 로깅 삭제하는 코드 개발 모드에서는 주석 처리
NoZyloDocsLogFilter().setup_logging()
HOST = os.getenv("SERVER_HOST", "localhost")
PORT = os.getenv("SERVER_PORT", "8000")

def set_initial_openapi_spec(app: FastAPI):
    openapi_json = app.openapi()
    app.state.openapi_service.set_current_spec(openapi_json)
    print(f"http://{HOST}:{PORT}/zylo-docs")

def add_zylo_docs(app: FastAPI):
    if not hasattr(app.state, 'openapi_service'):
        app.state.openapi_service = OpenApiService()
        
    app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "static")), name="static")

    app.include_router(front_route.router, prefix="/zylo-docs", tags=["front"])
    app.include_router(proxy_route.router, prefix="/zylo-docs/api", tags=["proxy"])
    app.add_middleware(ExceptionHandlingMiddleware)

    @app.get("/zylo-docs/{full_path:path}", include_in_schema=False)
    async def serve_react_app():
        return FileResponse(os.path.join(os.path.dirname(__file__), "static", "index.html"))

    set_initial_openapi_spec(app)

