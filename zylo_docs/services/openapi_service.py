from typing import Optional

class OpenApiService:
    def __init__(self):
        self.current_spec: Optional[dict] = None
        
    def set_current_spec(self, openapi_json: dict):
        self.current_spec = openapi_json
        
    def get_current_spec(self) -> dict:
        if self.current_spec is None:
            return {}
        return self.current_spec
        