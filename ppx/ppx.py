import requests
import re
import os
import time
from parsel import Selector

root = './mp4/'
from fake_useragent import UserAgent

# 生成对象
useragent = UserAgent()
headers = {
    'User-Agent': useragent.random
}


def get_url(num):
    url = 'https://www.pearvideo.com/popular_loading.jsp'
    data = {
        'reqType': 1,
        'categoryId': 59,
        'start': num
    }
    res = requests.get(url, headers=headers, params=data)
    s = Selector(text=res.content.decode())
    li_list = ['https://www.pearvideo.com/{}'.format(i) for i in s.xpath('//li/a[@class="actplay"]/@href').getall()]
    return li_list


def get_mp4(url):
    res = requests.get(url, headers=headers)
    s = Selector(text=res.content.decode())
    name = s.xpath('//h1[@class="video-tt"]/text()').get()
    pattern = re.compile(r'srcUrl="(.*?)"', re.S)
    mp4_url = pattern.findall(res.text)[0]
    print(name)
    dowm_mp4(name, mp4_url)


def dowm_mp4(name, url):
    if not os.path.exists(root):
        os.makedirs(root)
    res = requests.get(url, headers=headers)
    path = root + name + '.mp4'
    with open(path, 'wb') as f:
        f.write(res.content)
        print('下载成功')


def start():
    for i in range(10):  # 爬取十页
        urls = get_url(i)
        for url in urls:
            get_mp4(url)
            time.sleep(2)


start()