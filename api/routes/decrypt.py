from http import HTTPStatus
from fastapi import APIRouter, status, HTTPException

from models.decrypt import DecryptRequest, DecryptResponse
from services.ciphers import sipher_determiner, encryptors

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
        

@router.post('/json/file')
async def process_decrypt_data(key: str, file: UploadFile = File(...)):

    # try:
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
        pad_mode = gostcrypto.gostcipher.PAD_MODE_1 if 'pad_mode' not in algorithm or algorithm['pad_mode'] == 1 or algorithm['pad_mode'] == None else gostcrypto.gostcipher.PAD_MODE_2
        if algorithm['algorithm'] == 'kuznechik':
            cipher_obj = gostcrypto.gostcipher.new('kuznechik',
                                        key_bytes,
                                        algorithm['mode'],
                                        pad_mode=pad_mode)
            return DecryptResponse(
                info='kuznechik algorithm',
                encrypted_info=str(cipher_obj.encrypt(b'kuznechik algorithm'))
            )
        
        if algorithm['algorithm'] == 'magma':
            cipher_obj = gostcrypto.gostcipher.new('magma',
                                        key_bytes,
                                        algorithm['mode'],
                                        pad_mode=pad_mode)
            return DecryptResponse(
                info='magma algorithm',
                encrypted_info=str(cipher_obj.encrypt(b'magma algorithm'))
            )
        
        if algorithm['algorithm'] == 'aes':
            cipher = AES.new(key_bytes, algorithm['mode'])
            ei=cipher.encrypt(pad(b'aes algorithm', 16))
            return DecryptResponse(
                info='aes algorithm',
                encrypted_info=str(ei)
            )

        
    # except:
    #     # FIX: добавлен класс ошибки
    #     raise bad_decrypt_request()
