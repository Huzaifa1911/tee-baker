from typing import Any
from fastapi.responses import JSONResponse
import json


class DefaultResponse(JSONResponse):
    def render(self, content: Any) -> bytes:
        return json.dumps({"status": "success", "data": content}).encode("utf-8")
