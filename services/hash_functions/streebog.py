import gostcrypto

def get_hash(hash_string) -> bytes:
    hash_string = u'{hash_string}'.encode('cp1251')
    hash_obj = gostcrypto.gosthash.new('streebog256', data=hash_string)
    hash_result = bytes(hash_obj.digest())
    return hash_result