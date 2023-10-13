from enum import Enum

class GOSTAlgorithm(Enum):
    NONE: str = 'none'
    RSA: str = 'rsa'
    AES: str = 'aes'
    KUZNECHIK: str = 'kuznechik'
    MAGMA: str = 'magma'
    
class PadMode(Enum):
    PAD_MODE_1: int = 1
    PAD_MODE_2: int = 2

class BlockSize(Enum):
    AES: int = 16
    KUZNECHIK: int = 16
    MAGMA: int = 8