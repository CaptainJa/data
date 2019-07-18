# -*- coding: utf-8 -*-
# 多线程抓取店铺列表

from stem import Signal
from stem.control import Controller
import time
from lxml import etree
import requests
import re
import os
import threading
import json
import console
import splitter


class const():
    lock = threading.Lock()    # 控制同步

    TOR_DATA_PORT = 9050       # 代理数据端口
    TOR_CONTROL_PORT = 9051    # 代理控制端口
    TOR_PASSWORD = ''          # 代理控制密码
    PROXIES = {                # 代理服务器
        'http': 'socks5://localhost:%d' % (TOR_DATA_PORT),
        'https': 'socks5://localhost:%d' % (TOR_DATA_PORT)
    }

    SHOP_LIST_FILE = 'SHOP-LIST-12K-190225.JSON'        # 保存信息的文件
    USED_IP_FILE = 'USED_IP.HTML'                 # 保存已使用过的IP地址

    TARGET_URL = 'https://myip.ms/browse/sites/{PAGE_NUM}/ipID/23.227.38.0/ipIDii/23.227.38.255/sort/6/asc/1#sites_tbl_top'


# USED TO SHOW INFORMATION
class GetPageError(Exception):
    pass


# USED TO SHOW INFORMATION
class ExtractingInfoError(Exception):
    pass


# 多线程抓取操作
class ShadowCloneCrawler(threading.Thread):
    def __init__(self, name, page_num):
        threading.Thread.__init__(self)
        self.name = name
        self.page_num = page_num
        self.response = ''            # 储存响应信息
        self.shop_url_list = []

    def run(self):
        console.debug('{0} getting page ...'.format(self.page_num))
        flag = self.get_page(self.page_num)
        if flag is False:
            console.warning('FAILED TO GET PAGE: %04d' % (self.page_num))
        else:
            console.debug('{0} extracting info ...'.format(self.page_num))
            flag = self.extract_information()
            if flag is False:
                console.warning('FAILED TO EXTRACT INFO: %04d' %
                                (self.page_num))
            else:
                console.debug('{0} saving info ...'.format(self.page_num))
                # 用锁控制写入同步
                const.lock.acquire()
                self.save_shop_url_list()
                const.lock.release()
                console.debug('save done')

    def get_page(self, page_num):
        '''
        获取页面数据
        '''
        try:
            url = const.TARGET_URL.format(PAGE_NUM=page_num)
            self.response = requests.get(url, proxies=const.PROXIES)
        except GetPageError('failed to get page: %d' % (page_num)):
            return False
        else:
            if self.response.status_code is 200:
                return True
            else:
                return False

    def extract_information(self):
        '''
        提取数据：店铺网址、排名、访问量
        '''
        try:
            html = etree.HTML(self.response.text)
            path_table = '//table[@id= "sites_tbl"]/tbody/tr'
            table = html.xpath(path_table)

            for row_num in range(0, len(table), 2):
                items_main_row = table[row_num]
                path_shop_level = './td[1]/text()'
                path_shop_addr = './td[2]/a/text()'
                path_shop_rank = './td[7]/span/text()'
                shop_level = items_main_row.xpath(path_shop_level)[0]
                shop_addr = items_main_row.xpath(path_shop_addr)[0]
                shop_rank = items_main_row.xpath(path_shop_rank)[0]
                shop_rank = re.sub(r'[#,\s]', '', shop_rank)

                items_sub_row = table[row_num+1]
                path_shop_visits = './td/div[2]/span/text()'
                shop_visits = items_sub_row.xpath(path_shop_visits)[0]
                shop_visits = re.sub(r'[#,\s]', '', shop_visits)

                self.shop_url_list.append(
                    [shop_level, shop_addr, shop_rank, shop_visits])
        except ExtractingInfoError('Failed to extract information!'):
            return False
        else:
            if len(self.shop_url_list) == 50:  # 判断信息是否齐全
                return True
            else:
                return False

    def save_shop_url_list(self):
        '''
        把数据保存到文件
        '''
        with open(const.SHOP_LIST_FILE, 'a') as file:
            item_name = 'page-%04d' % (self.page_num)
            data = {item_name: self.shop_url_list}
            data_string = json.dumps(data)
            file.write(data_string)

        self.shop_url_list.clear()


def send_signal_to_change_ip():
    '''
    更换IP
    '''
    with Controller.from_port(port=const.TOR_CONTROL_PORT) as controller:
        controller.authenticate(password=const.TOR_PASSWORD)
        controller.signal(Signal.NEWNYM)
        time.sleep(controller.get_newnym_wait())


def change_ip():
    '''
    更换IP后，检查是否已经使用过。
    如果以前用过，需要另换一个，直到获取未使用过的IP为止。
    '''
    IP_TEST_URL = 'http://api.ipify.org?format=json'

    while True:
        try:
            send_signal_to_change_ip()
            response = requests.get(IP_TEST_URL, proxies=const.PROXIES)
        except Exception as ee:
            console.error('error during change ip')
            console.error('REASON: %s' % (str(ee)))
            time.sleep(0.5)
        else:
            if response.status_code == 200:
                data = json.loads(response.text)
                new_ip_string = data['ip'] + '\n'

                with open(const.USED_IP_FILE, 'r') as file:
                    used_ips = file.readlines()
                    file.close()

                if new_ip_string not in used_ips:
                    with open(const.USED_IP_FILE, 'a') as file:
                        file.write(new_ip_string)
                        file.close()
                    print('CURRENT IP: %s' % (data['ip']))
                    break
            else:
                console.debug('retry...')


def start_to_crawl_pages(start_page, end_page):
    START_PAGE = start_page
    END_PAGE = end_page
    thread_numbers = 15

    # 如果历史IP文件不存在，则创建
    if not os.path.exists(const.USED_IP_FILE):
        with open(const.USED_IP_FILE, 'w') as file:
            file.close()

    # 读取已经存取的列表
    if os.path.exists(const.SHOP_LIST_FILE):
        with open(const.SHOP_LIST_FILE, 'r') as file:
            content = file.read()
            file.close()
        pat = r'page-(\d{4})'
        existing_pages = re.findall(pat, content)
        existing_pages = [int(num) for num in existing_pages]
        skip_list = list(set(existing_pages))
    else:
        skip_list = []

    # 去除已经抓取的页面
    param_pages = list(range(START_PAGE, END_PAGE+1))
    param_pages_set = set(param_pages)
    skip_list_set = set(skip_list)
    remain_pages_set = param_pages_set - skip_list_set
    remain_pages = list(remain_pages_set)

    # 开启多线程，抓取页面数据
    blocks = splitter.split_to_blocks(remain_pages, thread_numbers)
    coal_miners = []
    for block in blocks:
        # 更换IP
        console.debug('Switch a new ip...')
        change_ip()

        # 进行多线程抓取
        coal_miners.clear()
        for page_num in block:
            name = 'clone-{0}'.format(page_num)
            worker = ShadowCloneCrawler(name, page_num)
            coal_miners.append(worker)

        for woker in coal_miners:
            woker.start()

        for woker in coal_miners:
            woker.join()

    # 整理保存的文件，去除重复项，并整理成JSON标准格式
    with open(const.SHOP_LIST_FILE, 'r') as file:
        content = file.read()
        file.close()
    pat = r'\{[^}]*?\}'
    items = set(re.findall(pat, content))
    data_list = [json.loads(item) for item in items]
    data_list_string = json.dumps(data_list)
    with open(const.SHOP_LIST_FILE, 'w') as file:
        file.write(data_list_string)
        file.close()


# ================================= #
# 抓取前200个页面的店铺信息
# 即流量排名前10000的店铺
# 对于10000以后的店铺，日访问量低于500，基本属于长尾店铺
# 从竞争分析的角度，暂时没必要关注
if __name__ == '__main__':
    console.info('start the crawler')
    start_to_crawl_pages(start_page=1, end_page=400)
    console.info('finished')
