from pydantic import BaseModel
from typing import Any

class DecryptRequest(BaseModel):
    key: str
    body: str
    code: str

class DecryptResponse(BaseModel):
    info: str
    encrypted_info: str