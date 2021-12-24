import os
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
import json

class EncryptDecrypt():
    def __init__(self, directory):
        self.cryptdir = directory
        self.key = None
        self.chunks = 32 * 1024

    def encryptDict(self, dictdata):
        if type(dictdata) is not dict:
            print("Not a Dictionary")
            return
        if self.key is None:
            print("set key first")
            return
        data = json.dumps(dictdata).encode("utf-8")
        filesz = str(len(data)).zfill(16).encode("utf-8")
        IV = Random.new().read(16)
        encrypter = AES.new(self.key, AES.MODE_CFB, IV)
        outdata = b''
        i = 0
        while True:
            tempdata = data[0 + self.chunks * i: self.chunks + self.chunks * i]
            if len(tempdata) == 0:
                break
            if len(tempdata) % 16 != 0:
                tempdata += b' ' * (16 - len(tempdata))
            outdata += encrypter.encrypt(tempdata)
            i = i + 1
        return (filesz, IV, outdata)

    def writeFile(self, fname, filesz, IV, encdata):
        with open(os.path.join(self.cryptdir, fname), 'wb') as fwrite:
            fwrite.write(filesz)
            fwrite.write(IV)
            fwrite.write(encdata)

    def setNewKey(self, key):
        self.key = SHA256.new(key.encode('utf-8')).digest()

    def decryptFile(self, file):
        with open(os.path.join(self.cryptdir, file),'rb') as encfile:
            filesz = int(str(encfile.read(16), "utf-8"))
            IV = encfile.read(16)
            decrypter = AES.new(self.key, AES.MODE_CFB, IV)
            outdata = b''
            while True:
                temdata = encfile.read(self.chunks)
                if len(temdata) == 0:
                    break
                outdata += decrypter.decrypt(temdata)
            outdata = outdata[0:filesz]
            return outdata
    def decrypt(self):
        pass

if __name__ == "__main__":
    pass
    #encdec = EncryptDecrypt("test")
    #dict = {"id": "04",
    #        "1": "0"}
    #encdec.encrypt(dict)
    