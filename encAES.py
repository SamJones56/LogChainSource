from Crypto.Cipher import AES
import os

def encAes(data):
        data.encode()
        key = os.urandom(32)
        cipher = AES.new(key, AES.MODE_EAX)

        nonce = cipher.nonce
        ciphertext, tag = cipher.encrypt_and_digest(data)

        return(key.hex(),nonce.hex(),ciphertext.hex())
