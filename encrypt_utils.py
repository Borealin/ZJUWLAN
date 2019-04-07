from Crypto.Cipher import AES
import base64

key = b'\x8c#\x18N\x11\xe2\xd9O\x0c.*\xeedg&o'


def encrypt(data):
    data = bytes(data, 'utf-8')
    while len(data) % 64 != 0:
        data += b' '
    cipher = AES.new(key, AES.MODE_EAX)
    nonce = cipher.nonce
    ciphertext, tag = cipher.encrypt_and_digest(data)
    return nonce, ciphertext, tag


def decrypt(nonce, ciphertext, tag):
    cipher = AES.new(key, AES.MODE_EAX, nonce)
    data = cipher.decrypt_and_verify(ciphertext, tag)
    data = str(data, 'utf-8')
    data.rstrip(' ')
    return data
