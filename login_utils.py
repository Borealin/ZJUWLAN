# -*- coding:utf-8 -*-
import re
import time
import requests
import requests.exceptions
import storage_utils

login_url = 'https://net.zju.edu.cn/include/auth_action.php'
form_data = {
    'action': 'login',
    'username': '',
    'password': '',
    'ac_id': '3',
    'user_ip': '',
    'nas_ip': '',
    'user_mac': '',
    'save_me': '1',
    'ajax': '1'
}
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/67.0.3396.99 Safari/537.36'}


def login(username, password):  # 登陆net.zju.edu.cn并处理返回的异常
    result = url_login(username, password)
    status_code = result['code']
    text = result['text']
    if status_code != 200:
        print('请检查是否开启全局代理或更改了DNS')
        return
    else:
        login_ok = re.match('login_ok', text)  # 成功登陆
        interval = re.match('.*interval', text)  # 异常：两次登陆需间隔10秒
        ip_exception = re.match('E2833', text)  # 异常：ip地址异常，请重新拿ip地址
        wrong_password = re.match('E2901', text)  # 异常： 密码错误
        if login_ok is not None:
            print('成功登陆')
        elif interval is not None:
            time.sleep(8)
            login(username, password)
        elif ip_exception is not None:
            print('有线网请不要使用net.zju.edu.cn登陆')
        elif wrong_password is not None:
            print('密码错误请重新输入密码')
            storage_utils.build_config()
            time.sleep(8)
            instant_login()


def url_login(username, passwd):  # post登陆表单
    s = requests.session()
    data = form_data
    data['username'] = username
    data['password'] = passwd
    try:
        response = s.post(login_url, data=data, headers=header)
    except ConnectionError:
        return {
            'code': 0,
            'text': ''
        }
    return {
        'code': response.status_code,
        'text': response.text
    }


def instant_login():  # 立即登陆
    auth = storage_utils.get_auth()
    login(auth['name'], auth['pass'])
