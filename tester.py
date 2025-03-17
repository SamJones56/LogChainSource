from aesController import decAes

kyberCipherTextHex = ""
nonceHex = ""
cipherTextHex = ""

decrypted = decAes(kyberCipherTextHex, nonceHex, cipherTextHex)

print(decrypted)