from http import HTTPStatus
from fastapi import APIRouter, status, HTTPException

from .auth import get_user_keys

from models.decrypt import DecryptRequest, DecryptResponse
from services.ciphers import sipher_determiner, encryptors
from models.auth import LoginRequest
from resources import GOSTAlgorithm, PadMode, BlockSize

from api.exceptions import bad_decrypt_request, undetectable_cipher

from fastapi import APIRouter, status, HTTPException, File, UploadFile
from fastapi.responses import StreamingResponse, FileResponse
import gostcrypto
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

router = APIRouter()
# распознает тип шифра только на зашифрованном json файле ключом private_key
# алгоритмами AES, кузнечик и магма в разных режимах
# но классы расчитаны и на получение всех данных извне (ключа тоже)
        

@router.post('/json/key')
async def process_decrypt_data(key: str, file: UploadFile = File(...)):

    try:
        encrypted_data_bytes = await file.read()
        encrypted_data = bytearray(encrypted_data_bytes)
        sd = sipher_determiner.sipher_determiner(key)
        algorithm = sd(encrypted_data)
        if (algorithm == None or algorithm['algorithm'] == 'none'): 
            # FIX: добавлен класс ошибки
            raise undetectable_cipher()
            # return DecryptResponse(
            #     info="can't determine algorithm",
            #     encrypted_info=""
            # )

        key_bytes = encryptors.to_bytes(key)
        pad_mode = gostcrypto.gostcipher.PAD_MODE_1 if 'pad_mode' not in algorithm or algorithm['pad_mode'] == PadMode.PAD_MODE_1 or algorithm['pad_mode'] == None else gostcrypto.gostcipher.PAD_MODE_2
        if algorithm['algorithm'] == GOSTAlgorithm.KUZNECHIK:
            cipher_obj = gostcrypto.gostcipher.new('kuznechik',
                                        key_bytes,
                                        algorithm['mode'],
                                        pad_mode=pad_mode)
            return DecryptResponse(
                info='kuznechik algorithm',
                encrypted_info=str(cipher_obj.encrypt(b'kuznechik algorithm'))
            )
        
        if algorithm['algorithm'] == GOSTAlgorithm.MAGMA:
            cipher_obj = gostcrypto.gostcipher.new('magma',
                                        key_bytes,
                                        algorithm['mode'],
                                        pad_mode=pad_mode)
            return DecryptResponse(
                info='magma algorithm',
                encrypted_info=str(cipher_obj.encrypt(b'magma algorithm'))
            )
        
        if algorithm['algorithm'] == GOSTAlgorithm.AES:
            cipher = AES.new(key_bytes, algorithm['mode'])
            ei=cipher.encrypt(pad(b'aes algorithm', BlockSize.AES))
            return DecryptResponse(
                info='aes algorithm',
                encrypted_info=str(ei)
            )

        
    except:
        # FIX: добавлен класс ошибки
        raise bad_decrypt_request()


@router.post('/json/name')
async def decrypt_by_name(name : str, file : UploadFile = File(...)) -> DecryptResponse:
    keys = await get_user_keys(LoginRequest(name=name))

    for key in keys:
        try:
            algorithm = await process_decrypt_data(key, file)
            if algorithm is None:
                continue
            else:
                return algorithm
        except:
            continue