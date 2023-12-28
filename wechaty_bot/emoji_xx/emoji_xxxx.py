import asyncio
import os
import random
from bs4 import BeautifulSoup
from syncer import sync
from comment import pyppeteer_demo,proxy_util
import requests

emoji_path="https://image.baidu.com/search/index?tn=baiduimage&ct=201326592&lm=-1&cl=2&ie=gb18030&word=%B1%ED%C7%E9%B0%FC&fr=ala&ala=1&alatpl=normal&pos=0&dyTabStr=MCwzLDEsMiw2LDQsNSw4LDcsOQ%3D%3D"


save_path='F:\\test_voice\\test_pic\\emoji'
if os.path.exists(save_path):os.mkdir(save_path)    # 创建文件夹



def save_pic(url,name):
    headers = {'User-Agent': random.choice(proxy_util.headers), 'Referer': url}
    img = requests.get(url, headers=headers)
    print('开始保存图片', img)
    file_name=os.path.join(save_path,name)
    f = open(file_name, 'ab')
    f.write(img.content)
    print(file_name, '图片保存成功！')
    f.close()

async def  get_emoji():
    page,browser=await pyppeteer_demo.pyppeteer_test(emoji_path)
    network=await page.evaluate('''() => {
       return window.performance.getEntries();
     }''')
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