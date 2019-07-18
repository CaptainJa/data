import requests
from http import cookies
import re
import ipchanger
from multiprocessing.dummy import Process, Lock
import console


def download_list(url, headers, cookies, pagenum):
    res = requests.get(url,  headers=headers, cookies=cookies)
    content = res.text

    trs = re.findall('<tr >', content)
    lock.acquire()
    if len(trs) == 50:
        with open('page-%04d.txt' % pagenum, 'w', encoding='utf-8') as fp:
            fp.write(content)
        console.info('%04d' % pagenum)
    else:
        print('ERROR %04d' % (pagenum))
    lock.release()


class Worker(Process):
    def __init__(self, url, headers, cookies, pagenum):
        Process.__init__(self)
        self.url = url
        self.headers = headers
        self.cookies = cookies
        self.pagenum = pagenum

    def run(self):
        download_list(self.url, self.headers, self.cookies, self.pagenum)


cookie_string = '''
s2_csrf_cookie_name=3f76537f806c00f9b6b717ce1169e299; PHPSESSID=hidgom5jit67v896poaj0m63u0; sw=126.3; s2_uGoo=f27eb4af32aedc7d9b0195e2163429348523e070; s2_csrf_cookie_name=3f76537f806c00f9b6b717ce1169e299; sh=28.1
'''

# 处理cookie字符串
cookie_processor = cookies.SimpleCookie()
cookie_processor.load(cookie_string)


# 转成requests匹配的dict格式
cookies = {}
for key, morsel in cookie_processor.items():
    cookies[key] = morsel.value


headers = {
    'Host': 'myip.ms',
    'Referer': 'https://myip.ms/browse/sites/1/ipID/23.227.38.0/ipIDii/23.227.38.255/sort/6/asc/1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
}


lock = Lock()
controller = ipchanger.init()
worklist = []
for pagenum in range(113, 318, 15):
    ipchanger.change_ip(controller)

    for ticker in range(1, 16):
        url = 'https://myip.ms/ajax_table/sites/%d/ipID/23.227.38.0/ipIDii/23.227.38.255/sort/6/asc/1' % (
            pagenum+ticker)

        w = Worker(url,  headers=headers, cookies=cookies,
                   pagenum=pagenum+ticker)
        worklist.append(w)

    [w.start() for w in worklist]
    [w.join() for w in worklist]
    worklist.clear()
