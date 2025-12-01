import os
import base64

def generate_aes_key():
    key = os.urandom(32)  # AES-256
    return base64.b64encode(key).decode()

def decode_aes_key(key_str):
    return base64.b64decode(key_str)
