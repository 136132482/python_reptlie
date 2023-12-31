import asyncio
import base64
import io
import json
import os
import sys
import threading
import time
import random
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
# from selenium.webdriver.ie.options import Options
# from selenium.webdriver.firefox.options import Options
from selenium.webdriver.chrome.options import Options as chromOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options as edgeOptions
from selenium.webdriver.edge.service import Service as edgeService
from selenium.webdriver.chrome.service import Service as ChromeService
from browsermobproxy import Server
import paramiko
import subprocess
import httpx
import  pyhttpx
from wechaty_bot.emoji_xx import  emoji_xxxx
from comment import  pyppeteer_demo
requests.packages.urllib3.disable_warnings()
from PIL import Image

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
    # proxy = get_proxy()
    # chrome_options = chromOptions()
    # caps = DesiredCapabilities.CHROME
    # caps['goog:loggingPrefs'] = {'performance': 'ALL'}
    caps = {
        "browserName": "chrome",
        'goog:loggingPrefs': {'performance': 'ALL'}  # 开启日志性能监听
    }

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

def xh(brower):
   t = True
   time.sleep(1)
   while t:
      brower.execute_script("window.scrollBy(0,100)")
      try:
          # 滚动至元素ele可见位置
          eles = brower.find_element(By.CSS_SELECTOR,'#rs table tr th a')
          ele = eles[0]
          brower.execute_script("arguments[0].scrollIntoView();", ele)
          time.sleep(1)
          t = False
      except:
         xh(brower)


def get_winodws_scroll(brower):
    # 获取当前页面的高度
    last_height = brower.execute_script("return document.body.scrollHeight")
    network_list=[]
    # 模拟下拉操作，直到滑动到底部
    while True:
        network = brower.execute_script("return window.performance.getEntries();")
        print(len(network))
        brower.delete_all_cookies()
        network_list.extend(network_list)
        # 模拟下拉操作
        brower.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # 等待页面加载
        time.sleep(2)
        # 获取当前页面的高度
        new_height = brower.execute_script("return document.body.scrollHeight")
        # 判断是否已经到达页面底部
        if new_height == last_height:
            break
        # 继续下拉操作
        last_height = new_height
    return network_list

def  xlk(brower):
    network_list=[]
    for y in range(100):
        js = 'window.scrollBy(0,300)'
        brower.execute_script(js)
        # brower.delete_all_cookies()
        network = brower.execute_script("return window.performance.getEntries();")
        time.sleep(2)
        if  y==99:
          network_list.extend(network)
        print("数量为："+str(len(network)))
    return network_list
save_path=''
def get_href_network(url):
    brower =click(url)
    # brower.execute_script(pyppeteer_demo.pull_down_new)
    # network=xlk(brower)
    # network = brower.execute_script("return window.performance.getEntries();")
    # print("数量为：" + str(len(network)))
    network=get_winodws_scroll(brower)
    brower.close()
    data_list=[]
    count=0
    for data in network:
        if data['name'].startswith("https://"):
            if data['initiatorType']=='img':
                url=data['name']
                data_list.append(url)
                print(data)
                name=os.path.basename(url.split("?")[0])
                name=name.split(".")
                if len(name)>1:
                    name = str(count) + "." + name[1]
                else:
                    name = str(count) + ".jpg"
                emoji_xxxx.save_pic(url,name)
        if data['name'].startswith("data:image"):
                 url=data['name']
                 decode_base64_image(url,save_path,count)
        count+=1
def decode_base64_image(base64_string,path,i):
    data = base64_string.split(',')[1]
    format=base64_string.split(',')[0]
    format=format.split('/')[1]
    format=format.split(';')[0]
    path=os.path.join(path,str(i)+"."+format)
    image_data=base64.b64decode(data)
    image=Image.open(io.BytesIO(image_data))
    print(image)
    image.save(path,format)
if __name__=='__main__':
    # proxy=get_proxy()
    # print(proxy)
    get_href_network("https://image.baidu.com/search/index?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&fm=result&fr=&sf=1&fmq=1703833585535_R&pv=&ic=&nc=1&z=&hd=&latest=&copyright=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&dyTabStr=MCwzLDEsMiw2LDQsNSw4LDcsOQ%3D%3D&ie=utf-8&sid=&word=%E8%A1%A8%E6%83%85%E5%8C%85")

