from pydantic import BaseModel
from typing import Any

class EncryptRequest(BaseModel):
    key: str
    body: str

class EncryptResponse(BaseModel):
    body: str
    
class RSAEncryptResponse(BaseModel):
    key: Any
    body: Any