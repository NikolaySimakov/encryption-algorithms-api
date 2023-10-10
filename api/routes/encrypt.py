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
async def aes_encrypt(data: encrypt.EncryptRequest) -> encrypt.EncryptResponse:
    
    try:
        encrypted_data = encryptors.aes_encryptor(data.key, data.body)
        _hash = streebog.get_hash(data.body)
        
        return encrypt.EncryptResponse(
            key=data.key,
            body=str(encrypted_data),
            sign=str(_hash),
        )
    except:
        # FIX: добавлен класс ошибки
        raise bad_data_for_encrypt()


@router.post('/aes/file')
async def kuzneckik_file_encrypt(key: str, file: UploadFile = File(...)):
    
    try:
        
        file_bytes = await file.read()
        encrypted_data = encryptors.aes_encryptor(key, file_bytes)
        return StreamingResponse(io.BytesIO(encrypted_data), media_type='application/octet-stream')
    
    except:
        # FIX: добавлен класс ошибки
        raise bad_data_for_encrypt()


@router.post('/kuznechik')
async def kuznechik_encrypt(data: encrypt.EncryptRequest): 
# -> encrypt.EncryptResponse:
    # try:

        # 12345678901234567890123456789012

        encrypted_data = encryptors.kuznechik_encryptor(data.key, data.body)
        # print(encrypted_data)
        # key = encryptors.to_bytes(data.key)
        # cipher_obj = gostcrypto.gostcipher.new('kuznechik',
        #                                 key,
        #                                 gostcrypto.gostcipher.MODE_ECB,
        #                                 pad_mode=gostcrypto.gostcipher.PAD_MODE_1)

        # decrypted_data = cipher_obj.decrypt(encrypted_data)
        # print(decrypted_data)
        return StreamingResponse(io.BytesIO(encrypted_data), media_type='application/octet-stream')
        # _hash = streebog.get_hash(data.body)
        # return encrypt.EncryptResponse(
        #     key=data.key,
        #     body=encrypted_data,
        #     sign=_hash,
        # )
    # except Exception as e:
    #     # FIX: добавлен класс ошибки
    #     raise bad_data_for_encrypt()


@router.post('/kuznechik/file')
async def kuzneckik_file_encrypt(key: str, file: UploadFile = File(...)):
    
    try:
        file_bytes = await file.read()
        data = bytearray(file_bytes)
        encrypted_data = encryptors.kuznechik_encryptor(key, data)
        return StreamingResponse(io.BytesIO(encrypted_data), media_type='application/octet-stream')
        
    except:
        # FIX: добавлен класс ошибки
        raise bad_data_for_encrypt()



@router.post('/magma')
async def magma_encrypt(data: encrypt.EncryptRequest) -> encrypt.EncryptResponse:
    try:
        encrypted_data = encryptors.magma_encryptor(data.key, data.body)
        _hash = streebog.get_hash(data.body)
        return encrypt.EncryptResponse(
            key=data.key,
            body=encrypted_data,
            sign=_hash,
        )
    except:
        # FIX: добавлен класс ошибки
        raise bad_data_for_encrypt()
    
    
@router.post('/magma/file')
async def kuzneckik_file_encrypt(key: str, file: UploadFile = File(...)):
    try:
        
        file_bytes = await file.read()
        encrypted_data = encryptors.magma_encryptor(key, file_bytes, )
        return StreamingResponse(io.BytesIO(encrypted_data), media_type='application/octet-stream')

    except:
        # FIX: добавлен класс ошибки
        raise bad_data_for_encrypt()
