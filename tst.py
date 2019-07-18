import requests
from http import cookies
import re
import changer


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


ticker = 1
for pagenum in range(1, 301):
    ticker += 1
    if ticker == 19:
        ticker = 0
        changer.change_ip()

    url = 'https://myip.ms/ajax_table/sites/%d/ipID/23.227.38.0/ipIDii/23.227.38.255/sort/6/asc/1' % (
        pagenum)

    res = requests.get(url,  headers=headers, cookies=cookies)
    content = res.text

    trs = re.find_all('<tr >')
    if len(trs) == 50:
        with open('page-%04d.txt' % pagenum, 'w', encoding='utf-8') as fp:
            fp.write()
    else:
        print('ERROR %04d' % (pagenum))
