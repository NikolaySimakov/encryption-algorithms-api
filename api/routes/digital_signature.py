from enum import Enum
from typing import Any
from http import HTTPStatus
import io

from fastapi import APIRouter, status, HTTPException, File, UploadFile
from models import digital_signature
from services.digital_signatures import signature_process as _signature_create, signature_verify as _signature_verify
from services.ciphers.encryptors import to_bytes

from api.exceptions import bad_data_for_encrypt

router = APIRouter()

@router.post('/signature_process')
async def signature_process(data: digital_signature.DigitalSignatureProcessRequest) -> digital_signature.DigitalSignatureProcessResponse:
    try:
        sign = _signature_create(data.message, bytearray(to_bytes(data.private_key)))
        return digital_signature.DigitalSignatureProcessResponse(
            public_key=sign["public_key"],
            signed_message=sign["sign"]
        )
    except:
        # FIX: добавлен класс ошибки
        raise bad_data_for_encrypt()

@router.post('/signature_verify')
async def signature_verify(data: digital_signature.DigitalSignatureVerifyRequest) -> digital_signature.DigitalSignatureVerifyResponse:
    try:
        check = _signature_verify(message=data.message, sign=bytearray(to_bytes(data.signed_message)), public_key=bytearray(to_bytes(data.public_key)))
        return digital_signature.DigitalSignatureVerifyResponse(
            res=check
        )
    except:
        # FIX: добавлен класс ошибки
        raise bad_data_for_encrypt()

