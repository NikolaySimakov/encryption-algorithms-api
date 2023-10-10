from enum import Enum
from typing import Any
from http import HTTPStatus
import io
import gostcrypto

from fastapi import APIRouter, status, HTTPException, File, UploadFile
from fastapi.responses import StreamingResponse, FileResponse
from models import encrypt

from services.ciphers import encryptors
from services.hash_functions import streebog

from api.exceptions import bad_data_for_encrypt

router = APIRouter()

@router.post('/rsa')
async def rsa_encrypt(data: encrypt.EncryptRequest) -> encrypt.EncryptResponse:
    
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


@router.post('/aes')
async def aes_encrypt(key: str, file: UploadFile = File(...)):
#  -> encrypt.EncryptResponse:
    
    try:
        file_bytes = await file.read()
        encrypted_data = encryptors.aes_encryptor(key, file_bytes)
        return StreamingResponse(io.BytesIO(encrypted_data), media_type='application/octet-stream')
        # _hash = streebog.get_hash(data.body)
        
        # return encrypt.EncryptResponse(
        #     key=data.key,
        #     body=str(encrypted_data),
        #     sign=str(_hash),
        # )
    except:
        # FIX: добавлен класс ошибки
        raise bad_data_for_encrypt()

@router.post('/kuznechik')
async def kuznechik_encrypt(key: str, file: UploadFile = File(...)): 
# -> encrypt.EncryptResponse:
    try:
        # 12345678901234567890123456789012
        file_bytes = await file.read()
        input_array = bytearray(file_bytes)
        encrypted_data = encryptors.kuznechik_encryptor(key, input_array)
        return StreamingResponse(io.BytesIO(encrypted_data), media_type='application/octet-stream')
        # _hash = streebog.get_hash(data.body)
        # return encrypt.EncryptResponse(
        #     key=data.key,
        #     body=encrypted_data,
        #     sign=_hash,
        # )
    except Exception as e:
        # FIX: добавлен класс ошибки
        raise bad_data_for_encrypt()

@router.post('/magma')
async def magma_encrypt(key: str, file: UploadFile = File(...)):
#  -> encrypt.EncryptResponse:
    try:
        file_bytes = await file.read()
        input_array = bytearray(file_bytes)
        encrypted_data = encryptors.magma_encryptor(key, input_array)
        return StreamingResponse(io.BytesIO(encrypted_data), media_type='application/octet-stream')
        # _hash = streebog.get_hash(data.body)
        # return encrypt.EncryptResponse(
        #     key=data.key,
        #     body=encrypted_data,
        #     sign=_hash,
        # )
    except:
        # FIX: добавлен класс ошибки
        raise bad_data_for_encrypt()
    
