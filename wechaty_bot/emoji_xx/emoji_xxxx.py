import asyncio
import os
import random
from bs4 import BeautifulSoup
from syncer import sync
from comment import pyppeteer_demo,proxy_util,comment_util
import requests

from comment.pyppeteer_demo import pull_down_new

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

emoji_path="https://image.baidu.com/search/index?tn=baiduimage&ct=201326592&lm=-1&cl=2&ie=gb18030&word=%B1%ED%C7%E9%B0%FC&fr=ala&ala=1&alatpl=normal&pos=0&dyTabStr=MCwzLDEsMiw2LDQsNSw4LDcsOQ%3D%3D"


save_path='F:\\test_voice\\test_pic\\emoji'
headers = {'User-Agent': random.choice(headers)}

def save_pic(url,name):
    img = requests.get(url, headers=headers)
    print('开始保存图片', img)
    comment_util.createFile(save_path)
    file_name=os.path.join(save_path,name)
    f = open(file_name, 'ab')
    f.write(img.content)
    print(file_name, '图片保存成功！')
    f.close()

async def  get_emoji():
    page,browser=await pyppeteer_demo.pyppeteer_test(emoji_path)
    # await page.evaluate(pull_down_new)
    network=await page.evaluate(""" async ()=>{
             return window.performance.getEntries();
              }
    """)
    for data in network:
        print(data)
    # result=await page.evaluate("""'ul[class="imglist clearfix pageNum0"]', (listLeft) = > {
    #         const items = listLeft.querySelectorAll('li[class="imgitem"]');
    #         const dictionary = new Object();
    #          items.forEach(async (item) => {
    #          // 这里获取的是每一项数据，可以直接拿到信息
    #          const item_a_link = item.querySelector("a");
    #           //   获取图片链接
    #          const item_img_src = item_a_link
    #             .getAttribute("href");
    #           // 获取标题
    #         const item_title = item_a_link
    #          .getAttribute("href").innerText;
    #           dictionary.item_title = item_img_src;
    #          });
    #          return dictionary;
    # }      """)
    # print(result)

def get_image(list):
    for link in list:
       href= link.find('a').get('href')
       name=link.find('a').get('href').get_text()
       save_pic(href,name)

if __name__=="__main__":
    asyncio.get_event_loop().run_until_complete(get_emoji())