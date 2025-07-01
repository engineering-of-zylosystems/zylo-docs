import httpx
import json

async def get_user_schemas():
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
    print(f"openapi_data_from_8000: {openapi_data_from_8000}")
    return {
        "message": "8001번 포트의 API입니다.",
        "fetched_openapi_from_8000": openapi_data_from_8000,
        "error_fetching_openapi": error_message
    }

