from flask import current_app

def xor_crypt_decrypt(text: str) -> str:
    key = current_app.config['PHONE_SECRET']
    return "".join(chr(ord(c) ^ ord(key[i % len(key)])) for i, c in enumerate(text))