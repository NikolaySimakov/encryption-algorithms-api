from pydantic import BaseModel
from typing import Any

class EncryptRequest(BaseModel):
    key: str
    body: str

class EncryptResponse(BaseModel):
    body: Any
    
class RSAEncryptResponse(BaseModel):
    key: Any
    body: Any