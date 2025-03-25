# -*- coding: utf-8 -*-
import random
import socket
import time
from random import choice

import requests
import yaml
from ping3 import ping


def load_config(config_path="config.yaml"):
    with open(config_path, "r", encoding='utf-8') as f:
        return yaml.safe_load(f)


def generate_fake_ip(true_ip):
    base_ip = true_ip.split('.')
    while True:
        candidate = f"{base_ip[0]}.{base_ip[1]}.{random.randint(0, 255)}.{random.randint(0, 255)}"
        print('.', end='')
        if ping(candidate, size=64, timeout=1):
            return candidate


def send_request(template, params):
    try:
        resp = requests.get(template.format(**params), timeout=10)
        return resp.text
    except:
        return None


def perform_login(profile, user_info, ip, device_type=None):
    params = {
        'account': user_info['account'],
        'password': user_info['password'],
        'operator': user_info['operator'],
        'device': device_type if device_type else user_info['device'],
        'ip': ip
    }
    res = send_request(profile['login'], params)
    print("login", res)
    return res


def perform_logout(profile, user_info, ip):
    params = {
        'account': user_info['account'],
        'ip': ip
    }
    print("     ", send_request(profile['unbind'], params))
    print("     ", send_request(profile['logout'], params))

def perform_login_logout_cycle(profile, user_info, ip, device_type=None):
    perform_logout(profile, user_info, ip)
    time.sleep(3)
    perform_login(profile, user_info, ip, device_type)
    time.sleep(3)


def main():
    print("Waiting")
    config = load_config()
    true_ip = socket.gethostbyname(socket.gethostname())
    profile = config['profiles'][config['current_profile']]
    user_info = config['user_info']

    fake_ip = generate_fake_ip(true_ip)
    print('ok')
    print(true_ip)
    print(fake_ip)

    perform_login_logout_cycle(profile, user_info, true_ip, 1)
    perform_login_logout_cycle(profile, user_info, true_ip, 0)

    perform_logout(profile, user_info, true_ip)
    perform_logout(profile, user_info, fake_ip)

    print("1")
    choice= user_info['device']
    time.sleep(3)
    perform_login(profile, user_info, fake_ip, choice)
    time.sleep(3)
    perform_login(profile, user_info, true_ip, choice)


if __name__ == "__main__":
    main()
