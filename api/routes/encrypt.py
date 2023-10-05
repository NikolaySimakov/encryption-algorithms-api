from enum import Enum
from typing import Any
from http import HTTPStatus
import io

from fastapi import APIRouter, status, HTTPException, File, UploadFile
from fastapi.responses import StreamingResponse, FileResponse
from models import encrypt

from services.ciphers import encryptors

router = APIRouter()
# key = b'12345678901234567890123456789012' 

@router.post('/rsa')
async def rsa_encrypt(data: encrypt.EncryptRequest) -> encrypt.RSAEncryptResponse:
    
    try:
        private_key, encrypted_data = encryptors.rsa_encryptor(data.body)
        return encrypt.RSAEncryptResponse(
            key=private_key,
            body=encrypted_data,
        )
    except:
        # TODO: return error
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail={
                "error": "Invalid request",
            },
        )


@router.post('/aes')
async def aes_encrypt(data: encrypt.EncryptRequest) -> encrypt.EncryptResponse:
    
    try:
        encrypted_data = encryptors.aes_encryptor(data.key, data.body)
        
        return encrypt.EncryptResponse(
            body=str(encrypted_data)
        )
    except:
        # TODO: return error
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail={
                "error": "Invalid request",
            },
        )

@router.post('/aes/file')
async def kuzneckik_file_encrypt(key: str, file: UploadFile = File(...)):
    file_bytes = await file.read()
    encrypted_data = encryptors.aes_encryptor(key, file_bytes)
    return StreamingResponse(io.BytesIO(encrypted_data), media_type='application/octet-stream')



@router.post('/kuznechik')
async def kuznechik_encrypt(data: encrypt.EncryptRequest) -> encrypt.EncryptResponse:
    try:
        encrypted_data = encryptors.kuznechik_encryptor(data.key, data.body)
        print(encrypted_data)
        return encrypt.EncryptResponse(
            body=str(encrypted_data),
        )
    except Exception as e:
        # TODO: return error
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail={
                "error": e,
            },
        )

@router.post('/kuznechik/file')
async def kuzneckik_file_encrypt(key: str, file: UploadFile = File(...)):
    
    try:
        file_bytes = await file.read()
        encrypted_data = encryptors.kuznechik_encryptor(key, file_bytes)
        return StreamingResponse(io.BytesIO(encrypted_data), media_type='application/octet-stream')
    except:
        # TODO: return error
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail={
                "error": "Invalid request",
            },
        )



@router.post('/magma')
async def magma_encrypt(data: encrypt.EncryptRequest) -> encrypt.EncryptResponse:
    try:
        encrypted_data = encryptors.magma_encryptor(data.key, data.body)
        return encrypt.EncryptResponse(
            body=str(encrypted_data),
        )
    except:
        # TODO: return error
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail={
                "error": "Invalid request",
            },
        )
    
@router.post('/magma/file')
async def kuzneckik_file_encrypt(key: str, file: UploadFile = File(...)):
    try:
        
        file_bytes = await file.read()
        encrypted_data = encryptors.magma_encryptor(key, file_bytes, )
        return StreamingResponse(io.BytesIO(encrypted_data), media_type='application/octet-stream')

    except:
        # TODO: return error
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail={
                "error": "Invalid request",
            },
        )
