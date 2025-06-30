from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
import uvicorn
import httpx
from fastapi.middleware.cors import CORSMiddleware
import json

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/schemas")
async def read_root():
    target_url = "http://localhost:8000/openapi.json"
    openapi_data_from_8000 = None
    error_message = None

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(target_url)
            response.raise_for_status()  # 200 OK가 아니면 예외 발생
            openapi_data_from_8000 = response.json()
            print(f"successfully fetched OpenAPI data from {target_url}")

    except httpx.RequestError as exc:
        error_message = f"port 8000 server connection error {exc}"
        print(error_message)
    except json.JSONDecodeError:
        error_message = f"port 8000 server response is not valid JSON. URL: {target_url}"
        print(error_message)
    except Exception as exc:
        error_message = f"unknown error occurred: {exc}"
        print(error_message)

    return {
        "message": "8001번 포트의 API입니다.",
        "fetched_openapi_from_8000": openapi_data_from_8000,
        "error_fetching_openapi": error_message
    }

# 모든 경로에 대해 정적 프론트 서빙
@app.get("/{full_path:path}")
async def serve_react_app(full_path: str):
    print(f"Serving React app for path: {full_path}")
    return FileResponse("static/index.html")

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8001, reload=True)
