from typing import List, Optional

class OpenApiService:
    def __init__(self):
        self.openapi_json_list: List[dict] = []

    def set_latest(self, json: dict):
        self.openapi_json_list.append(json)

    def get_latest(self) -> dict:
        if self.openapi_json_list:
            return self.openapi_json_list[-1]
        return {}

# 싱글턴 인스턴스 생성
openapi_service = OpenApiService()
