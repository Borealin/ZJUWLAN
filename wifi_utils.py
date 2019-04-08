# -*- coding:utf-8 -*-
import binascii
import os
import re
import time


def wifi_search():  # 获取当前可搜索到的WiFi列表
    wifilist = []
    rawcmdlines = os.popen('netsh wlan show networks', 'r', 1)
    cmdlines = rawcmdlines.read()
    cells = re.findall(r'SSID(.*): (.*)\n', cmdlines)
    for cell in cells:
        wifilist.append(cell[1])
    return wifilist


def check_wifi_connection():  # 检查WiFi状态
    rawcmdlines = os.popen('netsh wlan show interfaces', 'r', 1)
    cmdlines = rawcmdlines.read()
    status = re.search(r'状态(.*):(.*)\n', cmdlines)
    if status.group().find('断开') != -1:  # WiFi未连接
        software_status = re.search(r'软件(.*)\n', cmdlines)
        if software_status.group().find('关') != -1:  # WiFi开关已关闭
            print('请打开WiFi')
            return False
        else:  # WiFi开关已开但尚未连接至任一WiFi
            connect_to_ZJUWLAN()
            return check_wifi_connection()
    elif status.group().find('已连接') != -1:
        return True
    else:
        print('出现未知错误')
        return False


def connect_to_wifi(ssid, password=None):  # 连接至指定ssid和密码的WiFi
    ifprofile = False
    cmdlines = os.popen('netsh wlan show profiles', 'r', 1).read()
    profiles = re.findall(r'(.*): (.*)\n', cmdlines)
    for profile in profiles:  # 检查是否曾经连接过该ssid的WiFi
        if profile[1] == ssid:
            ifprofile = True
    if not ifprofile:  # 未连接过该ssid的WiFi，创建并添加profile
        try:
            f = open('{}.xml', 'r'.format(ssid))
            f.close()
        except IOError:
            create_profile(ssid, password)
        os.popen('netsh wlan add profile filename=\"{}.xml\"'.format(ssid))
    os.popen('netsh wlan connect name={0} ssid={0}'.format(ssid))
    time.sleep(2)
    return


def get_wifi_name():  # 获取当前已连接WiFi的ssid
    if check_wifi_connection():
        cmdlines = os.popen('netsh wlan show interfaces', 'r', 1).read()
        ssid = re.findall(r'SSID(.*): (.*)\n', cmdlines)
        return ssid[0][1]
    else:
        return ''


def connect_to_ZJUWLAN():  # 连接至ZJUWLAN
    wifi_list = wifi_search()
    for wifi_name in wifi_list:
        if wifi_name == 'ZJUWLAN':
            connect_to_wifi('ZJUWLAN')
            return check_connection()
    print("ZJUWLAN不在wifi列表中")
    return False


def check_connection():  # 检查当前是否已连接至ZJUWLAN
    wifi_name = get_wifi_name()
    if wifi_name == 'ZJUWLAN':
        return True
    elif wifi_name == '':
        return False
    else:
        print('您已连接至其他网络\n正在连接至ZJUWLAN')
        connect_to_ZJUWLAN()
        time.sleep(3)
        return check_connection()


def create_profile(ssid, password):  # 创建profile
    hexssid = binascii.hexlify(ssid.encode("utf8")).upper()
    f = open('{}.xml'.format(ssid), 'w')
    authEncryption = '''
            <authEncryption>
				<authentication>{authentication}</authentication>
				<encryption>{encryption}</encryption>
				<useOneX>false</useOneX>
			</authEncryption>'''
    sharedKey = '''
    		<sharedKey>
    			<keyType>passPhrase</keyType>
    			<protected>{protected}</protected>
				<keyMaterial>{keyMaterial}</keyMaterial>
			</sharedKey>'''

    if password is None:
        authEncryption = authEncryption.format(authentication='open', encryption='none')
        sharedKey = ''
    else:
        authEncryption = authEncryption.format(authentication='WPA2PSK', encryption='AES')
        sharedKey = sharedKey.format(protected='false', keyMaterial=password)
    f.writelines('''<?xml version="1.0"?>
<WLANProfile xmlns="http://www.microsoft.com/networking/WLAN/profile/v1">
	<name>{ssid}</name>
	<SSIDConfig>
		<SSID>
			<hex>{hexssid}</hex>
			<name>{ssid}</name>
		</SSID>
	</SSIDConfig>
	<connectionType>ESS</connectionType>
	<connectionMode>auto</connectionMode>
	<MSM>
		<security>
{authEncryption}
{sharedKey}
		</security>
	</MSM>
</WLANProfile>'''.format(hexssid=hexssid.decode('utf-8'), ssid=ssid, authEncryption=authEncryption,
                         sharedKey=sharedKey))
    f.close()
