"""
Simple integration module for zylo-docs.
"""

from fastapi import APIRouter
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path

# Get the path to the static HTML file
STATIC_DIR = Path(__file__).parent / "static"
ZYLO_HTML = STATIC_DIR / "index.html"

def create_zylo_router():
    """Create a router for zylo-docs."""
    router = APIRouter()
    
    @router.get("/zylo", include_in_schema=False)
    async def zylo_ui():
        """Serve the Zylo Docs UI."""
        if ZYLO_HTML.exists():
            return FileResponse(ZYLO_HTML)
        else:
            return {"error": "Zylo Docs UI not found"}, 404
    
    return router

def mount_zylo_docs(app):
    """
    Mount zylo-docs into a FastAPI application.
    Args:
        app: The FastAPI application to mount zylo-docs into
    """
    router = create_zylo_router()
    app.include_router(router)
    
    # Mount static files using StaticFiles
    try:
        app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
    except Exception as e:
        print(f"Warning: Could not mount static files: {e}")
    
    print("🚀 Zylo Docs mounted at: /zylo")
    print("📖 UI available at: /zylo")
    print("📋 OpenAPI spec available at: /openapi.json")
    print("📁 Static files available at: /static/") 
