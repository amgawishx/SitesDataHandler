import base64 as b64
from hashlib import sha256
from Crypto import Random
from Crypto.Cipher import AES
class AESCipher(object):
    '''
    A class for encrypting and decrypting text using AES256 algorithm for
    cryptography.
    '''
    def __init__(self,key):
        self.bs=32
        self.key=sha256(key.encode()).digest()
    def enc(self,txt):
        '''
        The encrypting function.
        '''
        txt=self._pad(txt)
        iv=Random.new().read(AES.block_size)
        cipher=AES.new(self.key, AES.MODE_CBC, iv)
        return b64.b64encode(iv+cipher.encrypt(txt))
    def dec(self,enc):
        '''
        The decrypting function.
        '''
        enc=b64.b64decode(enc)
        iv=enc[:AES.block_size]
        cipher=AES.new(self.key,AES.MODE_CBC,iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')
    def _pad(self,s):
        return s+(self.bs-len(s)%self.bs)*chr(self.bs-len(s)%self.bs)
    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]
