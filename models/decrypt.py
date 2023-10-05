from pydantic import BaseModel
from typing import Any

class DecryptRequest(BaseModel):
    key: str
    body: str
    code: str

class DecryptResponse(BaseModel):
    key: Any = None
    body: str | bytes