# -*- coding:utf-8 -*-
import encrypt_utils

split_text = '+-*/bor/*-+'  # 储存学号和密码时的分隔符


def get_auth():  # 获取学号密码
    if check_storage():
        return read_config()
    else:
        build_config()
        return get_auth()


def check_storage():  # 检查是否储存过学号及密码
    try:
        f = open('config', 'rb')
        f.close()
    except IOError:
        return False
    return True


def read_config():  # 读取已储存的学号密码密钥
    f = open('config', 'rb')
    nonce, ciphertext, tag = [f.read(x) for x in (16, 64, -1)]
    f.close()
    data = encrypt_utils.decrypt(nonce, ciphertext, tag)
    name, password = data.split(split_text)
    return {
        'name': name,
        'pass': password
    }


def build_config():  # 建立并储存学号密码密钥
    name, password = enter_id_pass()
    data = name + split_text + password
    f = open('config', 'wb')
    nonce, ciphertext, tag = encrypt_utils.encrypt(data)
    [f.write(x) for x in (nonce, ciphertext, tag)]
    f.close()


def enter_id_pass():  # 输入并返回学号及姓名
    name = input("请输入学号")
    password = input("请输入校园网密码")
    return name, password
