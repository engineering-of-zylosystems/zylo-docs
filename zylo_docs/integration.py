import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from zylo_docs.schemas.response import APIResponse
from .routers import front_route, proxy_route 
from .middlewares.exception_handler import ExceptionHandlingMiddleware
from zylo_docs.services.openapi_service import OpenApiService 

EXTERNAL_API_BASE = "http://127.0.0.1:8000"
PROXY_PREFIX = "/zylo-docs/api"
def set_initial_openapi_spec(app: FastAPI):
    openapi_json = app.openapi()
    app.state.openapi_service.set_current_spec(openapi_json)

def add_zylo_docs(app: FastAPI):
    if not hasattr(app.state, 'openapi_service'):
        app.state.openapi_service = OpenApiService()
    
    app.include_router(front_route.router, prefix="/zylo-docs", tags=["schemas"])
    app.include_router(proxy_route.router, prefix="/zylo-docs/api", tags=["proxy"])
    app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "static")), name="static")
    app.add_middleware(ExceptionHandlingMiddleware)

    @app.get("/zylo-docs/{full_path:path}", include_in_schema=False)
    async def serve_react_app():
        print(f"Serving React app from {os.path.join(os.path.dirname(__file__), 'static', 'index.html')}")
        return FileResponse(os.path.join(os.path.dirname(__file__), "static", "index.html"))

    set_initial_openapi_spec(app)
#
