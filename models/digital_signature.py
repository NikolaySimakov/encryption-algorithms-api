from pydantic import BaseModel
from typing import Any

class DigitalSignatureRequest(BaseModel):
    body: str

class DigitalSignatureResponse(BaseModel):
    private_key: str
    public_key: str
    body: str
    