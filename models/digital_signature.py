from pydantic import BaseModel
from typing import Any

class DigitalSignatureProcessRequest(BaseModel):
    message: str
    private_key: str

class DigitalSignatureProcessResponse(BaseModel):
    public_key: str
    signed_message: str

class DigitalSignatureVerifyRequest(BaseModel):
    message: str
    signed_message: str
    public_key: str

class DigitalSignatureVerifyResponse(BaseModel):
    res: bool
