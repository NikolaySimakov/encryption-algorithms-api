from http import HTTPStatus
from fastapi import APIRouter, status, HTTPException

from models.decrypt import DecryptRequest, DecryptResponse
from services.ciphers import sipher_determiner

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
async def process_decrypt_data(file: UploadFile = File(...)):
    private_key = b'12345678901234567890123456789012' # for testing
    try:
        encrypted_data = await file.read()
        print(encrypted_data)
        sd = sipher_determiner(private_key)
        algorithm = sd(encrypted_data)
        if (algorithm == None or algorithm['algorithm'] == 'none'): 
            # FIX: добавлен класс ошибки
            raise undetectable_cipher()
            # return DecryptResponse(
            #     info="can't determine algorithm",
            #     encrypted_info=""
            # )
        
        if algorithm['algorithm'] == 'kuznechik':
            cipher_obj = gostcrypto.gostcipher.new('kuznechik',
                                        private_key,
                                        algorithm['mode'],
                                        pad_mode=algorithm['pad_mode'])
            return DecryptResponse(
                info='kuznechik algorithm',
                encrypted_info=str(cipher_obj.encrypt(b'kuznechik algorithm'))
            )
        
        if algorithm['algorithm'] == 'magma':
            cipher_obj = gostcrypto.gostcipher.new('magma',
                                        private_key,
                                        algorithm['mode'],
                                        pad_mode=algorithm['pad_mode'])
            return DecryptResponse(
                info='magma algorithm',
                encrypted_info=str(cipher_obj.encrypt(b'magma algorithm'))
            )
        
        if algorithm['algorithm'] == 'aes':
            cipher = AES.new(private_key, AES.MODE_ECB)
            ei=cipher.encrypt(pad(b'aes algorithm', 16))
            return DecryptResponse(
                info='aes algorithm',
                encrypted_info=str(ei)
            )

        
    except:
        # FIX: добавлен класс ошибки
        raise bad_decrypt_request()



@router.post('/')
async def process_decrypt_data(data: DecryptRequest):
    try:
        private_key = data.key
        encrypted_data = data.text
        
        sd = sipher_determiner(private_key)
        algorithm = sd(encrypted_data)
        if (algorithm == None or algorithm['algorithm'] == 'none'): 
            # FIX: добавлен класс ошибки
            raise undetectable_cipher()
            # return DecryptResponse(
            #     info="can't determine algorithm",
            #     encrypted_info=""
            # )
        
        if algorithm['algorithm'] == 'kuznechik':
            cipher_obj = gostcrypto.gostcipher.new('kuznechik',
                                        private_key,
                                        algorithm['mode'],
                                        pad_mode=algorithm['pad_mode'])
            return DecryptResponse(
                info='kuznechik algorithm',
                encrypted_info=str(cipher_obj.encrypt(b'kuznechik algorithm'))
            )
        
        if algorithm['algorithm'] == 'magma':
            cipher_obj = gostcrypto.gostcipher.new('magma',
                                        private_key,
                                        algorithm['mode'],
                                        pad_mode=algorithm['pad_mode'])
            return DecryptResponse(
                info='magma algorithm',
                encrypted_info=str(cipher_obj.encrypt(b'magma algorithm'))
            )
        
        if algorithm['algorithm'] == 'aes':
            cipher = AES.new(private_key, AES.MODE_ECB)
            ei=cipher.encrypt(pad(b'aes algorithm', 16))
            return DecryptResponse(
                info='aes algorithm',
                encrypted_info=str(ei)
            )

        
    except:
        # FIX: добавлен класс ошибки
        raise bad_decrypt_request()