from enum import Enum
from typing import Any
from http import HTTPStatus

from fastapi import APIRouter, status, HTTPException
from models import encrypt

from services.ciphers import encryptors

router = APIRouter()


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


@router.post('/kuznechik')
async def kuznechik_encrypt(data: encrypt.EncryptRequest) -> encrypt.EncryptResponse:
    try:
        encrypted_data = encryptors.kuznechik_encryptor(data.key, data.body)
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
