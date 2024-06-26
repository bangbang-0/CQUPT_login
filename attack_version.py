# -*- coding: utf-8 -*-
import random
import socket
import time
import webbrowser
from tkinter import messagebox

import psutil
import requests
from ping3 import ping


def get_ip_list():
    netcard_info = []
    info = psutil.net_if_addrs()
    for k, v in info.items():
        for item in v:
            if item[0] == 2 and not item[1] == '127.0.0.1':
                netcard_info.append((k, item[1]))
    return netcard_info


def getip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip


###仅供学习交流使用
def find_fake_ip():
    ip = '10.17.0.1'
    ip_list = ip.split('.')
    while True:
        i = random.randint(0, 255)
        j = random.randint(0, 255)
        fake_ip = f'{ip_list[0]}.{ip_list[1]}.{i}.{j}'
        if ping(fake_ip, size=1024, timeout=1):
            return fake_ip


def login(arg, ip, device):
    arg["ip"] = ip
    arg["device"] = device
    res = requests.get(
        'http://192.168.200.2:801/eportal/?c=Portal&a=login&callback=dr1003&login_method=1&user_account=%2C{device}%2C{account}%40{operator}&user_password={password}&wlan_user_ip={ip}&wlan_user_ipv6=&wlan_user_mac=000000000000&wlan_ac_ip=&wlan_ac_name='.format_map(
            arg))
    print('login ',res.text)
    if '"msg":""' in res.text:
        print('当前设备已登录 或 WiFi未连接')
        return
    elif r'\u8ba4\u8bc1\u6210\u529f' in res.text:
        re.append(1)
        if len(re) == 1:
            print('幸运儿登录成功', fake_ip)
        else:
            print('本地端登录成功', true_ip)
        return
    elif 'bGRhcCBhdXRoIGVycm9y' in res.text:
        print("密码错误")
        return
    elif 'aW51c2UsIGxvZ2luIGFnYWluL' in res.text:
        login(ip, arg)
    else:
        print("失败")


def logout(arg, ip):
    arg["ip"] = ip
    res = requests.get(
        'http://192.168.200.2:801/eportal/?c=Portal&a=unbind_mac&callback=dr1002&user_account={account}%40cmcc&wlan_user_mac=000000000000&wlan_user_ip={ip}'.format_map(
            arg))
    print(res.text)
    url = 'http://192.168.200.2:801/eportal/?c=Portal&a=logout&callback=dr1003&login_method=1&user_account=drcom&user_password=123&ac_logout=1&register_mode=1&wlan_user_ip={ip}&wlan_user_ipv6=&wlan_vlan_id=1&wlan_user_mac=000000000000&wlan_ac_ip=&wlan_ac_name=&jsVersion=3.3.3&v=9565'.format_map(
        data)
    html = requests.get(url, verify=False)

    print('\nlogout',html.text)
    if '"result":"1"' in html.text:
        print('注销成功')
    else:
        print('注销失败')


data = {"account": "***",  # 账号
        "password": "****",  # 密码
        "operator": "cmcc"}  # 运营商  默认移动cmcc   电信telecom  联通unicom

re = []
if __name__ == '__main__':
    true_ip = getip()
    fake_ip = find_fake_ip()
    logout(data, true_ip)
    time.sleep(3)
    login(data, true_ip, 1)
    time.sleep(3)
    logout(data, true_ip)
    time.sleep(3)
    login(data, true_ip, 0)
    time.sleep(3)
    logout(data, true_ip)
    re = []

    time.sleep(3)
    choice = 0
    login(data, fake_ip, choice)
    time.sleep(3)
    login(data, true_ip, choice)
    if len(re) == 2:
        if messagebox.askquestion('登录成功', '去测速吧，如果不行多试几次'):
            webbrowser.open('https://test.ustc.edu.cn/')
    else:
        messagebox.askquestion('登录失败', '再试一次吧')
