from http import HTTPStatus
from fastapi import APIRouter, status, HTTPException
from ...models import request, response
from ...services.ciphers import sipher_determiner
router = APIRouter()


@router.post('/json/string')
def process_encrypt_data(data : request) -> response:
    try:
        sd = sipher_determiner(data.key)
        res = sd(data.text)['algorithm']
        return {"info": res}
    except:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail={
                "error": "Invalid request",
            },
        )