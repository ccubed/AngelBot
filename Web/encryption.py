import base64
from Crypto.Cipher import AES
from Crypto import Random


class AESCipher:
    def __init__(self, key):
        self.key = key
        self.pad = lambda s: s + (16 - len(s) % 16) * chr(16 - len(s) % 16)
        self.unpad = lambda s: s[:-ord(s[len(s) - 1:])]

    def encrypt(self, raw):
        raw = self.pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:16]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self.unpad(cipher.decrypt(enc[16:]))
