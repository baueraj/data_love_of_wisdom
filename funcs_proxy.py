import requests
from lxml.html import fromstring
import random


def get_proxies(url, proxies_n):
    response = requests.get(url)
    parser = fromstring(response.text)
    proxies = set()
    for i in parser.xpath('//tbody/tr')[:proxies_n]:
        if i.xpath('.//td[7][contains(text(),"yes")]'):
            proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
            proxies.add(proxy)
    return list(proxies)


def get_proxy(url, proxies, timeout):
    while True:
        idx_proxy = random.randrange(len(proxies))
        proxy = proxies[idx_proxy]
        try:
            response = requests.get(url, proxies={"http": proxy, "https": proxy}) #, timeout=timeout
            print(response.json())
            return proxy
        except:
            print("Skipping. Connnection error or timeout")