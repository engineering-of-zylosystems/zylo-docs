import json
from pathlib import Path
from contextlib import asynccontextmanager
from fastapi import FastAPI

@asynccontextmanager
async def lifespan(app: FastAPI):
    await save_openapi_json(app)
    yield
    
async def save_openapi_json(app):
    base_dir = Path(__file__).resolve().parent
    data_dir = base_dir / "data"
    if not data_dir.exists():
        data_dir.mkdir(parents=True, exist_ok=True)
    file_path = data_dir / "all_schemas.json"
    if not file_path.exists():
        file_path.touch()
    response = app.openapi()
    openapi_json = response
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(openapi_json, f, indent=2, ensure_ascii=False)