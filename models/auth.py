from pydantic import BaseModel

class LoginRequest(BaseModel):
    name: str

class LoginResponse(BaseModel):
    name: str
    key: str

class AddKeyRequest(BaseModel):
    owner: str
    invited: str

class AddKeyResponse(BaseModel):
    result: bool