import json
import os
import sys
import threading
import time
import random
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
# from selenium.webdriver.ie.options import Options
# from selenium.webdriver.firefox.options import Options
from selenium.webdriver.chrome.options import Options as chromOptions
from selenium.webdriver.edge.options import Options as edgeOptions
from selenium.webdriver.edge.service import Service as edgeService
from selenium.webdriver.chrome.service import Service as ChromeService
from browsermobproxy import Server
import paramiko
import subprocess
import httpx
import  pyhttpx
requests.packages.urllib3.disable_warnings()

global headers
# 给请求指定一个请求头来模拟chrome浏览器
headers = [
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)",
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
    'Opera/9.25 (Windows NT 5.1; U; en)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
    'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
    'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
    'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
    "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7",
    "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0",
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'
]

# headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'}


headers = {'User-Agent': random.choice(headers)}


PROXY_POOL_URL = 'http://127.0.0.1:5010/get'


def get_proxy():
    try:
        response = requests.get(PROXY_POOL_URL)
        if response.status_code == 200:
            text= response.text
            text = json.loads(text)
            proxy=str(text['proxy'])
            return proxy
    except ConnectionError:
            return None


with open('E:\\stealth.min.js-main\\stealth.min.js', 'r') as f:
        js = f.read()
#开启Proxy：注意指定自己下载解压后路径
# server = Server(
#     r'F:\python_workspace\browsermob-proxy-2.1.4\bin\browsermob-proxy.bat')
# server.start()
# proxy = server.create_proxy()

def click(click_url):
    proxy = get_proxy()
    # chrome_options = chromOptions()
    chrome_options=webdriver.ChromeOptions()
    service = ChromeService(executable_path='C:\\Program Files\\Google\\Chrome\\Application\\chromedriver.exe')
    # chrome_options.add_argument("--headless")  # 不显示浏览器窗口
    chrome_options.add_argument('--disable-gpu')
    # chrome_options.add_experimental_option("debuggerAddress","127.0.0.1:8888")
    # chrome_options.add_argument('--incognito')
    chrome_options.add_argument('--ignore-certificate-errors')   # 禁用扩展插件
    chrome_options.add_argument('--ignore-urlfetcher-cert-requests')  # https需要加上，要不然回报安全连接问题
    # proxy.new_har("kgdxpr", options={'captureContent': True, 'captureContent': True, 'captureBinaryContent': True})
    # chrome_options.add_argument('--proxy-server={0}'.format(proxy))
    browser = webdriver.Chrome(service=service,options=chrome_options)
    browser.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {'source': js})
    browser.maximize_window()
    browser.implicitly_wait(20)
    browser.get(click_url)
    return browser




def click_noproxy(click_url):
    # proxy = get_proxy()
    chrome_options = chromOptions()
    # chrome_options=webdriver.ChromeOptions()
    service = ChromeService(executable_path='E:\\chromedriver-win64\\chromedriver.exe')
    # chrome_options.add_argument('--disable-gpu')
    # chrome_options.add_argument("--headless")  # 不显示浏览器窗口
    # chrome_options.add_argument('--incognito')
    # chrome_options.add_argument('--ignore-certificate-errors')   # 禁用扩展插件
    # chrome_options.add_argument('--ignore-urlfetcher-cert-requests')  # https需要加上，要不然回报安全连接问题
    # proxy.new_har("kgdxpr", options={'captureContent': True, 'captureContent': True, 'captureBinaryContent': True})
    # chrome_options.add_argument('--proxy-server={0}'.format(proxy.proxy))
    browser = webdriver.Chrome(service=service)
    browser.maximize_window()
    browser.implicitly_wait(20)
    browser.get(click_url)
    return browser
#获取html
def get_soup(url):
    proxy=get_proxy()
    proxies = {'http://': 'http://' + proxy, 'https://': 'https://' + proxy}
    # requests.urllib3.disable_warnings()
    res = requests.get(url, headers=headers,proxies=proxies, timeout=10, verify=False)
    html = res.content
    html_doc = str(html, 'utf8')
    bf = BeautifulSoup(html_doc, 'html.parser')
    return bf


if __name__=='__main__':
    proxy=get_proxy()
    print(proxy)

