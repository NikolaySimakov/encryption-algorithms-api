from enum import Enum
from typing import Any
from http import HTTPStatus
import io

from fastapi import APIRouter, status, HTTPException, File, UploadFile
from fastapi.responses import StreamingResponse
from models import digital_signature
from services.digital_signatures import signature_process as _signature_process, signature_verify as _signature_verify, generate_key as _generate_key
from services.ciphers.encryptors import to_bytes

from api.exceptions import bad_data_for_encrypt

router = APIRouter()

@router.post('/signature_process')
async def signature_process(data: digital_signature.DigitalSignatureProcessRequest) -> digital_signature.DigitalSignatureProcessResponse:
    # try:
        sign = _signature_process(message=data.message, private_key=bytearray(to_bytes(data.private_key, "cp1251")))
        return StreamingResponse(io.BytesIO(sign), media_type='application/octet-stream')
    # except:
    #     # FIX: добавлен класс ошибки
    #     raise bad_data_for_encrypt()

@router.post('/generate_public_key')
async def generate_public_key(data: digital_signature.GeneratePublicKeyRequest):
    try:
        public_key = _generate_key(bytearray(to_bytes(data.private_key, "cp1251")))
        return StreamingResponse(io.BytesIO(public_key), media_type='application/octet-stream')
    except:
        raise bad_data_for_encrypt()
          

@router.post('/signature_verify')
async def signature_verify(data: digital_signature.DigitalSignatureVerifyRequest) -> digital_signature.DigitalSignatureVerifyResponse:
    try:
        check = _signature_verify(message=data.message, sign=bytearray(to_bytes(data.signed_message, "cp1251")), public_key=bytearray(to_bytes(data.public_key, "cp1251")))
        return digital_signature.DigitalSignatureVerifyResponse(
            res=check
        )
    except:
        # FIX: добавлен класс ошибки
        raise bad_data_for_encrypt()

