from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import storage_utils
import pickle

key_file = 'key'


def key_init():  # 获取随机16位密钥
    key = get_random_bytes(16)
    return key


def read_key():  # 从已有的文件中获取密钥
    kf = open(key_file, 'rb')
    key = pickle.load(kf)
    kf.close()
    return key


def write_key(key):  # 写入密钥
    kf = open(key_file, 'wb')
    pickle.dump(key, kf)
    kf.close()


def get_key():  # 获取密钥
    try:
        key = read_key()
    except IOError:
        key = key_init()
        write_key(key)
    return key


def check_key():  # 检查并获取密钥
    try:
        key = read_key()
        return key
    except IOError:
        print('config密钥丢失，请重新输入信息')
        storage_utils.build_config()
        return False


def encrypt(data):  # 加密文本
    key = get_key()
    data = bytes(data, 'utf-8')
    while len(data) % 64 != 0:
        data += b' '
    cipher = AES.new(key, AES.MODE_EAX)
    nonce = cipher.nonce
    ciphertext, tag = cipher.encrypt_and_digest(data)
    return nonce, ciphertext, tag


def decrypt(nonce, ciphertext, tag):  # 解密文本
    key = check_key()
    if not key:
        return False
    cipher = AES.new(key, AES.MODE_EAX, nonce)
    data = cipher.decrypt_and_verify(ciphertext, tag)
    data = data.rstrip(b' ')
    data = str(data, 'utf-8')
    return data
