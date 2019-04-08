from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import storage_utils
import pickle

key_file = 'key'


def key_init():
    key = get_random_bytes(16)
    return key


def read_key():
    f = open(key_file, 'rb')
    key = pickle.load(f)
    f.close()
    return key


def write_key(key):
    f = open(key_file, 'wb')
    pickle.dump(key, f)
    f.close()


def get_key():
    try:
        key = read_key()
    except IOError:
        key = key_init()
        write_key(key)
    return key


def check_key():
    try:
        key = read_key()
        return key
    except IOError:
        print('config密钥丢失，请重新输入信息')
        storage_utils.build_config()
        return check_key()


def encrypt(data):
    key = get_key()
    data = bytes(data, 'utf-8')
    while len(data) % 64 != 0:
        data += b' '
    cipher = AES.new(key, AES.MODE_EAX)
    nonce = cipher.nonce
    ciphertext, tag = cipher.encrypt_and_digest(data)
    return nonce, ciphertext, tag


def decrypt(nonce, ciphertext, tag):
    key = check_key()
    cipher = AES.new(key, AES.MODE_EAX, nonce)
    data = cipher.decrypt_and_verify(ciphertext, tag)
    data.rstrip(b' ')
    data = str(data, 'utf-8')
    return data
