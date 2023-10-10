import rsa
import gostcrypto
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto import Random
import hashlib

from typing import Tuple


def to_bytes(key: str | bytes, code="utf-8") -> bytes:
    if type(key) == str:
        return key.encode(code)
    return key


def rsa_encryptor(body: str | bytes) -> Tuple[rsa.key.PrivateKey, str]:
    
    '''
    For decoding message you should use private key
    that's why I return two values
    '''
    
    public_key, private_key = rsa.newkeys(512)
    encrypted = rsa.encrypt(to_bytes(body), public_key)
    return private_key, encrypted


def aes_encryptor(
    key: str | bytes,
    raw: str | bytes,
) -> bytes:
    
    '''
    TODO: потом доделаю все остальное
    '''
    key = to_bytes(key)
    # key = hashlib.sha256(to_bytes(key)).digest()
    
    # def _pad(s):
    #     return s + (AES.block_size - len(s) % AES.block_size) * chr(AES.block_size - len(s) % AES.block_size)
    
    # raw = _pad(raw)
    # iv = Random.new().read(AES.block_size)
    # cipher = AES.new(key, AES.MODE_CBC, iv)
    # return bytes(iv + cipher.encrypt(to_bytes(raw)))

    cipher = AES.new(key, AES.MODE_ECB)
    encrypted_data = cipher.encrypt(pad(raw, 16))

    return encrypted_data

def kuznechik_encryptor(
    key: str | bytes,
    input_array : str | bytes | bytearray,
    block_size : int = 16,
    mode : int = gostcrypto.gostcipher.MODE_ECB,
    pad_mode_arg: int = 1,
    code="utf-8",
):
    key = to_bytes(key, code)
    input_arr = to_bytes(input_array, code)
    
    pad_mode = gostcrypto.gostcipher.PAD_MODE_1 if pad_mode_arg == 1 else gostcrypto.gostcipher.PAD_MODE_2
    cipher_obj = gostcrypto.gostcipher.new('kuznechik',
                                        key,
                                        mode,
                                        pad_mode=pad_mode)
    
    return cipher_obj.encrypt(input_arr)


def magma_encryptor(
    key: str | bytes,
    input_array : str | bytes | bytearray,
    block_size : int = 8, 
    mode: int = gostcrypto.gostcipher.MODE_ECB,
    pad_mode_arg: int = 1,
    code="utf-8",
):
    
    key = to_bytes(key, code)
    input_arr = to_bytes(input_array, code)
    
    pad_mode = gostcrypto.gostcipher.PAD_MODE_1 if pad_mode_arg == 1 else gostcrypto.gostcipher.PAD_MODE_2
    cipher_obj = gostcrypto.gostcipher.new('magma',
                                        key,
                                        mode,
                                        pad_mode=pad_mode)
    
    return cipher_obj.encrypt(input_arr)
