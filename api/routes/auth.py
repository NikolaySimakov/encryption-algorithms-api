from enum import Enum
from typing import Any
from http import HTTPStatus
import io
import gostcrypto

from services.tools import generators

from fastapi import APIRouter, status, HTTPException, File, UploadFile
from fastapi.responses import StreamingResponse, FileResponse
from models import encrypt, auth, schemas

from services.ciphers import encryptors
from services.hash_functions import streebog

from api.exceptions import bad_data

from fastapi_sqlalchemy import db

router = APIRouter()

@router.post('/new')
async def login_new_user(data: auth.LoginRequest) -> auth.LoginResponse:
    
    try:
        
        user = db.session.query(schemas.User).filter_by(name=data.name).first()
        if user != None:
            key_user = db.session.query(schemas.KeyUser).filter_by(id=user.id).first()
            key = db.session.query(schemas.Key).filter_by(id=key_user.key_id).first()
            return auth.LoginResponse(
                name=data.name,
                key=key.value
            )

        private_key = schemas.Key(
            value=generators.generate_random_string()
        )
        
        db.session.add(private_key)
        db.session.flush()

        new_user = schemas.User(
            name=data.name
        )
        new_user.keys.append(private_key)

        db.session.add(new_user)
        db.session.flush()

        db.session.commit()

        return auth.LoginResponse(
            name=new_user.name,
            key=private_key.value
        )
    except:
        # FIX: добавлен класс ошибки
        raise bad_data()


@router.post('/add_key')
async def add_key_to_user(data: auth.AddKeyRequest) -> auth.AddKeyResponse:
    try:
        owner = db.session.query(schemas.User).filter_by(name=data.owner).first()
        invited = db.session.query(schemas.User).filter_by(name=data.invited).first()

        if owner is None or invited is None:
            raise bad_data()
        
        owner_key_values = []
        owner_keys = db.session.query(schemas.User).filter_by(name=data.invited).first().keys
        for key in owner_keys:
            owner_key_values.append(key.value)

        keys = db.session.query(schemas.User).filter_by(name=data.invited).first().keys
        for key in keys:
            owner.keys.append(key)
            db.session.commit()


        return auth.AddKeyResponse(
            result=True
        )

    except:
        raise bad_data()


@router.post('/keys')
async def get_user_keys(data: auth.LoginRequest):
    try:
        
        keys = db.session.query(schemas.User).filter_by(name=data.name).first().keys
        result = []

        for key in keys:
            result.append(key.value)

        return result

    except:
        raise bad_data()
    