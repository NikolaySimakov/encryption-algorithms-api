from fastapi import HTTPException

class bad_data(HTTPException):
    def __init__(self, detail: str = None):
        super().__init__(status_code=400, detail=detail or "Bad data")