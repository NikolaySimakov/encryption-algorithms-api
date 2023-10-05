from pydantic import BaseModel


class DecryptRequest(BaseModel):
    key: str
    text: str


class DecryptResponse(BaseModel):
    info: str