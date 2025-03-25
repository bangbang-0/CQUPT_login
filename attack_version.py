# -*- coding: utf-8 -*-
import random
import socket
import time
import requests
from ping3 import ping


def find_fake_ip():
    a, b, *_ = true_ip.split('.')
    while True:
        i = random.randint(0, 255)
        j = random.randint(0, 255)
        res = f'{a}.{b}.{i}.{j}'
        print(res)
        if ping(res, size=1024, timeout=1):
            return res


def login(arg, ip, device):
    arg["ip"] = ip
    arg["device"] = device
    res = requests.get(
        'https://login.cqu.edu.cn:802/eportal/portal/login?callback=dr1004&user_account=%2C{device}%2C{account}&user_password={password}&wlan_user_ip={ip}'.format_map(
            arg))
    print('login ', res.text)


def logout(arg, ip):
    arg["ip"] = ip
    res = requests.get(
        'https://login.cqu.edu.cn:802/eportal/portal/mac/unbind?callback=dr1005&user_account={account}&wlan_user_ip={ip}'.format_map(
            arg))
    print(res.text)
    url = 'https://login.cqu.edu.cn:802/eportal/portal/logout?callback=dr1006&wlan_user_ip={ip}'.format_map(
        arg)
    html = requests.get(url)
    print(html.text)


data = {
    "account": "xxx",  # 账号
    "password": "xxx", #密码
    "operator": "cmcc"# 运营商  默认移动cmcc   电信telecom  联通unicom
}

if __name__ == '__main__':
    true_ip = socket.gethostbyname(socket.gethostname())
    fake_ip = find_fake_ip()
    print(fake_ip)

    logout(data, true_ip)
    time.sleep(3)
    login(data, true_ip, 1)
    time.sleep(3)
    logout(data, true_ip)
    time.sleep(3)
    login(data, true_ip, 0)
    time.sleep(3)
    logout(data, true_ip)

    time.sleep(3)
    choice = 0
    print('...')
    login(data, fake_ip, choice)
    time.sleep(3)
    login(data, true_ip, choice)
