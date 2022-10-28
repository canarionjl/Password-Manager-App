import os
import binascii
from json import JSONDecodeError

from cryptography.fernet import Fernet
import hashlib
import base64

word = "password".encode('utf-8')
hashes = hashlib.sha256(word).digest()
result = base64.urlsafe_b64encode(hashes)
print(result)

result_test = base64.urlsafe_b64encode(os.urandom(32))
print(result_test)


def encrypt_vault(key):
    try:
        with open("data.json", "rb") as vault:
            contents = vault.read()
            contents_decrypted = Fernet(key).encrypt(contents)
        with open("data.json", "wb") as vault:
            vault.write(contents_decrypted)
    except FileNotFoundError:
        pass
    except JSONDecodeError:
        pass


def decrypt_vault(key):
    with open("data.json", "rb") as vault:
        contents = vault.read()
        contents_decrypted = Fernet(key).decrypt(contents)
    with open("data.json", "wb") as vault:
        vault.write(contents_decrypted)


decrypt_vault(result)
