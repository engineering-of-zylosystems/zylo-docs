# zylo_docs/server_components.py
import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from zylo_docs.schemas.response import APIResponse
from .routers import front_api 
from .middlewares.exception_handler import ExceptionHandlingMiddleware

def add_zylo_docs(app: FastAPI):

    app.include_router(front_api.router, prefix="/zylo-docs", tags=["schemas"])
    app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "static")), name="static")
    app.add_middleware(ExceptionHandlingMiddleware)
    @app.get("/zylo-docs", include_in_schema=False)
    async def serve_react_app():
        print(f"Serving React app from {os.path.join(os.path.dirname(__file__), 'static', 'index.html')}")
        return FileResponse(os.path.join(os.path.dirname(__file__), "static", "index.html"))


    @app.get("/zylo/health", include_in_schema=False)
    def health_check():
        return APIResponse(
            success=True,
            message="Zylo-hub-be API server is running.",
            data=None
        )
    