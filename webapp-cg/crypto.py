import base64
import hashlib
import os
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Util.Padding import pad, unpad

# AES encryption
def aes_encrypt(message, key):
    iv = os.urandom(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted = cipher.encrypt(pad(message.encode(), AES.block_size))
    hmac = hashlib.sha256(encrypted + key).hexdigest()
    return base64.b64encode(iv + encrypted + hmac.encode()).decode()

def aes_decrypt(data, key):
    try:
        raw = base64.b64decode(data)
    except:
        return "ERROR: Corrupted data"
    iv = raw[:16]
    encrypted = raw[16:-64]
    hmac_received = raw[-64:].decode()
    hmac_calc = hashlib.sha256(encrypted + key).hexdigest()
    if hmac_calc != hmac_received:
        return "ERROR: Integrity check failed"
    cipher = AES.new(key, AES.MODE_CBC, iv)
    try:
        decrypted = unpad(cipher.decrypt(encrypted), AES.block_size)
        return decrypted.decode()
    except:
        return "ERROR: Wrong key or corrupted data"

# RSA encryption
def rsa_generate_keys():
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key, public_key

def rsa_encrypt(message, public_key):
    key = RSA.import_key(public_key)
    cipher = PKCS1_OAEP.new(key)
    encrypted = cipher.encrypt(message.encode())
    return base64.b64encode(encrypted).decode()

def rsa_decrypt(encrypted_data, private_key):
    key = RSA.import_key(private_key)
    cipher = PKCS1_OAEP.new(key)
    try:
        decrypted = cipher.decrypt(base64.b64decode(encrypted_data))
        return decrypted.decode()
    except:
        return "ERROR: Wrong key or corrupted data"
