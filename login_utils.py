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


def login(username, password):
    result = url_login(username, password)
    status_code = result['code']
    text = result['text']
    if status_code != 200:
        print('please check your connection')
        return
    else:
        login_ok = re.match('login_ok', text)
        interval = re.match('.*interval', text)
        ip_exception = re.match('E2833', text)
        wrong_password = re.match('E2901', text)
        if login_ok is not None:
            print('successful login')
        elif interval is not None:
            time.sleep(8)
            login(username, password)
        elif ip_exception is not None:
            print('please use l2tp to connect')
        elif wrong_password is not None:
            print('请重新输入密码')
            storage_utils.build_config()
            time.sleep(8)
            instant_login()


def url_login(username, passwd):
    s = requests.session()
    data = form_data
    data['username'] = username
    data['password'] = passwd
    try:
        response = s.post(login_url, data=data, headers=header)
    except ConnectionError:
        print('please connect to ZJUWLAN')
        return {
            'code': 0,
            'text': ''
        }
    return {
        'code': response.status_code,
        'text': response.text
    }


def instant_login():
    auth = storage_utils.get_auth()
    login(auth['name'], auth['pass'])
