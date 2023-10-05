from pydantic import BaseModel
from typing import Any

class EncryptRequest(BaseModel):
    key: str
    body: str

class EncryptResponse(BaseModel):
    key: str
    body: str
    sign: str
    