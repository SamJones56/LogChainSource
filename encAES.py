from Crypto.Cipher import AES
import os

def encAes(data):
        encKey = os.urandom(32)
        cipher = AES.new(encKey, AES.MODE_EAX)

        nonce = cipher.nonce
        ciphertext, tag = cipher.encrypt_and_digest(data)

        return(encKey,nonce,ciphertext)
