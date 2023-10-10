from gostcrypto.gostsignature import new, MODE_256, GOST34102012, CURVES_R_1323565_1_024_2019
from services.hash_functions.streebog import get_hash

def signature_process(message: str, private_key: bytearray) -> map:
    digest = bytearray(get_hash(message))
    sign_obj = new(MODE_256, CURVES_R_1323565_1_024_2019['id-tc26-gost-3410-2012-256-paramSetB'])    
    sign = sign_obj.sign(private_key=private_key, digest=digest)

    public_key = sign_obj.public_key_generate(private_key=private_key)

    return {
        "public_key": public_key,
        "sign": sign
    }

def signature_verify(message: str, sign: bytearray, public_key: bytearray) -> bool:
    digest = bytearray(get_hash(message))
    sign_obj = new(MODE_256, CURVES_R_1323565_1_024_2019['id-tc26-gost-3410-2012-256-paramSetB'])
    
    if sign_obj.verify(public_key=public_key, digest=digest, signature=sign):
        return True
    else:
        return False
