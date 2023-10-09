from fastapi import HTTPException

class undetectable_cipher(HTTPException):
    def __init__(self, detail: str = None):
        super().__init__(status_code=400, detail=detail or "Can't determine algorithm")