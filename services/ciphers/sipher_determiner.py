from typing import Any
import gostcrypto
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from ..tools.validators import remove_fillers, is_decodable, check_empty, check_json_item, is_valid_json

class sipher_determiner:

    def __init__(self, key: str | bytes, code="utf-8"):
        if (type(key) == str):
            self.key = key.encode(code)
        else:
            self.key = key

    def try_gost_algorithm(
            self,
            name: str,
            input_array : bytes | bytearray, 
            block_size : int, 
            mode : int,
            pad_mode_arg=1,
            code="utf-8"):
        
        if pad_mode_arg == 2:
            cipher_obj = gostcrypto.gostcipher.new(
                        name,
                        self.key,
                        mode,
                        pad_mode=gostcrypto.gostcipher.PAD_MODE_2
                    )
        else:
            cipher_obj = gostcrypto.gostcipher.new(
                        name,
                        self.key,
                        mode,
                        pad_mode=gostcrypto.gostcipher.PAD_MODE_1
                    )
        
        # решено отказаться от этого алгоритма ввиду производительности
        # for i in range(0, len(input_array), block_size):
        #     end_idx = min(len(input_array), (i + block_size))
        #     decrypted_block = cipher_obj.decrypt(input_array[i:end_idx])
        #     decrypted_block = remove_fillers(decrypted_block)
        #     if is_decodable(decrypted_block):
        #         decrypted_str = decrypted_block.decode(code)
        #         if check_empty(decrypted_str):
        #             continue
        #         if check_json_item(decrypted_str):
        #             res = remove_fillers(cipher_obj.decrypt(input_array))
        #             if is_decodable(res):
        #                 res = res.decode(code)
        #             if (is_valid_json(res)):
        #                 return {'algorithm' : name, 'mode': mode}

        decrypted_array = remove_fillers(cipher_obj.decrypt(input_array))
        if is_decodable(decrypted_array):
            if is_valid_json(decrypted_array):
                return {'algorithm' : name, 'mode': mode, 'pad_mode': pad_mode_arg}
                    
        return {'algorithm' : 'none'}

    def kuznechik_check(self, input_array: bytes | bytearray, code="utf-8"):

        for mode in range(1, 7):
            if (mode == 4):
                continue
            res = self.try_gost_algorithm('kuznechik', input_array, 16, mode, 1, code)
            if (res != None and res['algorithm'] != 'none'):
                return {'algorithm' : 'kuznechik', 'mode': mode, 'pad_mode': 1}
            if mode == 1 or mode == 2:
                res = self.try_gost_algorithm('kuznechik', input_array, 16, mode, 2, code)
                if (res['algorithm'] != 'none'):
                    return {'algorithm' : 'kuznechik', 'mode': mode, 'pad_mode': 2}

    def magma_check(self, input_array: bytes | bytearray, code="utf-8"):

        for mode in range(1, 7):
            if (mode == 4):
                continue
            res = self.try_gost_algorithm('magma', input_array, 8, mode, 1, code)
            if (res != None and res['algorithm'] != 'none'):
                return {'algorithm' : 'magma', 'mode': mode, 'pad_mode': 1}
            if mode == 1 or mode == 2:
                res = self.try_gost_algorithm('magma', input_array, 8, mode, 2, code)
                if (res['algorithm'] != 'none'):
                    return {'algorithm' : 'magma', 'mode': mode, 'pad_mode': 2}

    def aes_check(self, input_array: bytes, code="utf-8"):

        for mode in range(1, 12):
            if mode == 4 or mode == 10:
                continue
            # for i in range(0, len(input_array), block_size):
            #     end_idx = (i + block_size)
            #     if len(input_array[i:end_idx]) != block_size:
            #         continue
            #     cipher_obj = AES.new(key, mode)
            #     decrypted_block = cipher_obj.decrypt(input_array[i:end_idx])
            #     if is_decodable(decrypted_block):
            #         decrypted_str = decrypted_block.decode(code)
            #         if check_json_item(decrypted_str):
            #             res = cipher_obj.decrypt(input_array)
            #             res = unpad(res, block_size)
            #             if is_decodable(res):
            #                 res = res.decode(code)
            #             if (is_valid_json(res)):
            #                 return {'algorithm' : 'aes', 'mode': mode}

            cipher_obj = AES.new(self.key, mode)
            decrypted_array = unpad(cipher_obj.decrypt(input_array), 16)

            if is_decodable(decrypted_array):
                if is_valid_json(decrypted_array):
                    return {'algorithm' : 'aes', 'mode': mode}
                    
        return {'algorithm' : 'none'}

    def __call__(self, 
                 input_array: str | bytes | bytearray,
                 code="utf-8", 
                 *args: Any, **kwds: Any) -> str:
        
        if (type(input_array) == str):
            input_array = input_array.encode(code)
        try:
            res = self.kuznechik_check(input_array, code)
            if (res != None and res['algorithm'] != 'none'):
                return res

            res = self.magma_check(input_array, code)
            if (res != None and res['algorithm'] != 'none'):
                return res
            
            res = self.aes_check(input_array, code)
            if (res != None and res['algorithm'] != 'none'):
                return res
        except:
            return {'algorithm' : 'none'}
        
        