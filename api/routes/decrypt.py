from http import HTTPStatus
from fastapi import APIRouter, status, HTTPException

from models import decrypt
from services.ciphers import sipher_determiner


router = APIRouter()


@router.post('/json/string')
def process_decrypt_data(data: decrypt.DecryptRequest) -> decrypt.DecryptResponse:
    try:
        sd = sipher_determiner(data.key)
        res = sd(data.body)['algorithm']
        return decrypt.DecryptResponse(
            info=res,
        )
    except:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail={
                "error": "Invalid request",
            },
        )