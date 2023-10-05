from pydantic import BaseModel

class request(BaseModel):
    text: str
    key: str