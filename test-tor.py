# -*- coding: utf-8 -*-
import socks
import socket
from stem import Signal
from stem.control import Controller
import time
import requests
import console


def TorIPChanger():
    def __init__(self):
        TOR_CONTROL_PORT = 9051
        TOR_DATA_PORT = 9050
        PASSWORD = '12345'
        self.controller = Controller.from_port(port=TOR_CONTROL_PORT)
        self.controller.authenticate(PASSWORD)

        socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5,
                              '127.0.0.1',
                              TOR_DATA_PORT,
                              True)
        socket.socket = socks.socksocket

    def change_ip(self):
        console.info('Waiting for new ip...')
        self.controller.signal(Signal.NEWNYM)
        time.sleep(self.controller.get_newnym_wait())
        console.info('IP changed')


if __name__ == '__main__':
    ipchanger = TorIPChanger()

    url = 'http://ipecho.net/plain'
    res = requests.get(url)
    print(res.text)

    ipchanger.change_ip()
    res = requests.get(url)
    print(res.text)
