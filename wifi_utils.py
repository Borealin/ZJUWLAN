import os
import re
import time


def wifi_search():
    wifilist = []
    cells = wifi.Cell.all('wlan0')
    for cell in cells:
        wifilist.append(cell)
    return wifilist


def check_wifi_connection():
    rawcmdlines = os.popen('netsh wlan show interfaces', 'r', 1)
    cmdlines = rawcmdlines.read()
    status = re.search(r'状态(.*):(.*)\n', cmdlines)
    if status.group().find('断开') != -1:
        print('请打开WiFi')
        return 0
    elif status.group().find('已连接') != -1:
        return 1
    else:
        print('出现未知错误')
        return 2


def connet_to_wifi(ssid, password=None):
    return


def get_wifi_name():
    if check_wifi_connection() == 1:
        cmdlines = os.popen('netsh wlan show interfaces', 'r', 1).read()
        ssid = re.findall(r'SSID(.*): (.*)\n', cmdlines)
        return ssid[0][1]
    else:
        return ''


def connect_to_ZJUWLAN():
    wifi_list = wifi_search()
    for wifi_name in wifi_list:
        if wifi_name == 'ZJUWLAN':
            connet_to_wifi('ZJUWLAN')
            return check_connection()
    return False


def check_connection():
    wifi_name = get_wifi_name()
    if 'ZJUWLAN' in wifi_name:
        return True
    elif wifi_name == '':
        return False
    else:
        print('您尚未连接至ZJUWLAN\n正在连接至ZJUWLAN')
        time.sleep(5)
        connect_to_ZJUWLAN()
