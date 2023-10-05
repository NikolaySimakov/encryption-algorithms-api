from http import HTTPStatus
from fastapi import APIRouter, status, HTTPException
from models.decrypt import DecryptRequest, DecryptResponse
from services.ciphers import sipher_determiner, encryptors

router = APIRouter()


@router.post('/json/message')
def process_decrypt_data(data : DecryptRequest):
    try:
        private_key, encrypted_data = data.key.encode(data.code), data.body(data.code)
        sd = sipher_determiner(private_key, data.code)
        algorithm = sd(encrypted_data, data.code)
        if (algorithm == None or algorithm['algorithm'] == 'none'): 
            return DecryptResponse(
                info="can't determine algorithm"
            )
        return DecryptResponse(
            info=algorithm['algorithm']
        )
        
    except:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail={
                "error": "Invalid request",
            },
        )