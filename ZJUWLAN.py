# -*- coding:utf-8 -*-
import time
import wifi_utils
import login_utils

connect_status = wifi_utils.check_connection()
while not connect_status:
    input('输入任意字符继续')
    connect_status = wifi_utils.check_connection()
login_utils.instant_login()
time.sleep(1)
