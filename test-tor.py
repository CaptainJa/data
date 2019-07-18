# -*- coding: utf-8 -*-
import socks
import socket
from stem import Signal
from stem.control import Controller
import time
import requests
import console

TOR_CONTROL_PORT = 9051
TOR_DATA_PORT = 9050
PASSWORD = '12345'
        
def init():
    print('init...')
    controller = Controller.from_port(port=TOR_CONTROL_PORT)
    controller.authenticate(PASSWORD)
    socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5,
                              '127.0.0.1',
                              TOR_DATA_PORT,
                              True)
    socket.socket = socks.socksocket
    print('init over')
    return controller

def change_ip(controller):
    if True:
        console.info('Waiting for new ip...')
        controller.signal(Signal.NEWNYM)
        time.sleep(controller.get_newnym_wait())
        console.info('IP changed')


if __name__ == '__main__':
    controller = init()

    url = 'http://ipecho.net/plain'
    res = requests.get(url)
    print(res.text)

    change_ip(controller)
    res = requests.get(url)
    print(res.text)
