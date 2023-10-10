from enum import Enum
from typing import Any
from http import HTTPStatus
import io

from fastapi import APIRouter, status, HTTPException, File, UploadFile
from models import digital_signature

from services.ciphers import encryptors
from services.hash_functions import streebog

from api.exceptions import bad_data_for_encrypt

router = APIRouter()

@router.post('/')
async def create_digital_signature(data: digital_signature.DigitalSignatureRequest) -> digital_signature.DigitalSignatureResponse:
    
    try:
        private_key, encrypted_data = encryptors.rsa_encryptor(data.body)
        _hash = streebog.get_hash(data.body)
        return encrypt.EncryptResponse(
            key=str(private_key),
            body=str(encrypted_data),
            sign=str(_hash),
        )
    except:
        # FIX: добавлен класс ошибки
        raise bad_data_for_encrypt()
