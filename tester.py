from aesController import decAes

kyberCipherTextHex = ""
nonceHex = ""
cipherTextHex = ""
tag = ""

decrypted = decAes(kyberCipherTextHex, nonceHex, cipherTextHex, tag)

print(decrypted)