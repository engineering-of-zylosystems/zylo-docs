from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from app.schemas.response import APIResponse
from app.routers import schemas
import uvicorn


app = FastAPI(title="Zylo Docs API",)

app.mount("/static", StaticFiles(directory="static"), name="static")
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
    return FileResponse("static/index.html")

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8001, reload=True)
