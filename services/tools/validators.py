import re
import json

def is_valid_json(json_str : str):
    try:
        json.loads(json_str)
        return True
    except ValueError:
        return False
    
def is_decodable(byte_array: bytes, encoding='utf-8'):
    try:
        byte_array.decode(encoding)
        return True
    except UnicodeDecodeError:
        return False

def remove_fillers(byte_array: bytes):
    return byte_array.replace(b'\x80', b'').replace(b'\x00', b'')

def check_json_item(input_str):
    pattern = r'^[\s]*\{.*$'
    if re.match(pattern, input_str):
        return True
    else:
        return False
    
def check_empty(string):
    pattern = r'^[ \t\n]+$'
    if re.search(pattern, string):
        return True
    else:
        return False