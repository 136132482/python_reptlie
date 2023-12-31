import asyncio
import json
import os
import re
import time
import uuid
from io import BytesIO
from urllib.parse import urlsplit
from pyppeteer import launch
from bs4 import BeautifulSoup
from pyppeteer_stealth import stealth
from pyppeteer.network_manager import Request, Response
from pyquery import PyQuery as pq
# from comment.proxy_util import get_proxy

from pyppeteer import launcher
from PIL import Image
import requests

from comment.proxy_util import get_proxy
from wechaty_bot.emoji_xx.emoji_xxxx import *
try:
    launcher.AUTOMATION_ARGS.remove("--enable-automation")
except:
    pass
try:
    launcher.DEFAULT_ARGS.remove("--enable-automation")
except:
    pass
from pyppeteer import launch


BASE_DIR = os.path.dirname(__file__)

# async def add_intercept(page):
#     await page.setRequestInterception(True)
#     page.on('request', PageMiddleware.intercept_request)
#     page.on('response',PageMiddleware.intercept_response)


async def intercept_request(req):
    print("request url", req.url)
    print("request type", req.resourceType)
    await get_url(req)
    if req.resourceType in ['stylesheet', 'script', 'image', 'media', 'eventsource', 'websocket']:
        await req.abort()
    else:
        await req.continue_()

async  def  get_url(req):
     if req.resourceType=='image':
         emoji = emoji_xxxx()
         name=str(uuid.uuid4())
         await emoji.save_pic(req.url,name)

async def intercept_response(res):
    resourceType = res.request.resourceType
    print("response type", resourceType)
    if resourceType in ['xhr', 'fetch','img']:
        resp = await res.text()
        print("这是data:" + resp)
        resp=json.loads(resp)
        if type(resp)==dict:
                list=resp['data']
                for img in list:
                    if 'thumbURL' in img:
                        url=img['thumbURL']
                        emoji = emoji_xxxx()
                        name = str(uuid.uuid4())
                        await emoji.save_pic(url,name)

        # if 'https://img' in resp:
        #     print(resp)
        #     content = await resp.text()
        #     title = re.search(b"<title>(.*?)</title>", content)
        #     print(title.group(1))
    #     tokens = urlsplit(url)
    #     folder = BASE_DIR + '/' + 'data/' + tokens.netloc + tokens.path + "/"
    #     if not os.path.exists(folder):
    #         os.makedirs(folder, exist_ok=True)
    #     filename = os.path.join(folder, str(int(time.time())) + '.json')
    #     with open(filename, 'w', encoding='utf-8') as f:
    #         f.write(resp)


async def pyppeteer_test(url):
    # proxy = get_proxy()
    # print(proxy)
    # executablePath = pyppeteer.executablePath()
    # print('自动下载的 chromium 的存储位置为：', executablePath)
    browser = await launch(
        headless=False,  # 如果为False, 则会打开浏览器界面，适合在有界面的机器上观察浏览器行为
        executablePath="C:\Program Files\Google\Chrome\Application\chrome.exe",
        # 也可以指定为机器上的已安装的 Chrome 浏览器： r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
        args=[
            # '--no-sandbox'
            '--disable-extensions',
            '--hide-scrollbars',
            '--disable-bundled-ppapi-flash',
            '--mute-audio',
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-gpu',
            # 浏览器铺满屏幕
            #'--start-fullscreen',
            # 窗口在浏览器中最大化(mac测试无效)
            #'--start-maximized'
             # f'--proxy-server={proxy}'
        ]
    )
    page = await browser.newPage()
    # await page.setRequestInterception(True)
    # page.on('request', intercept_request)
    # page.on('response', intercept_response)
    await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                            '(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299')

    await page.setViewport({'width': 1920, 'height': 1080})  # 调整页面的尺寸为 1920*1080
    await page.setJavaScriptEnabled(enabled=True)  # 允许 javascript 执行
    await stealth(page)
    await page.goto(
        url,
        waitUntil='networkidle0'  # 直到未结束的网络连接数为 0，停止等待。（可以用来等待 ajax 结束）
    )
    js_text = """
    () =>{
        Object.defineProperties(navigator,{ webdriver:{ get: () => false } });
        window.navigator.chrome = { runtime: {},  };
        Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] });
        Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5,6], });
     }
        """
    await page.evaluateOnNewDocument(js_text)
    # doc = pq(await page.content())
    # print('Quotes:', doc('.quote').length)
    # await page.evaluate("""
    #             () =>{
    #                    Object.defineProperties(navigator,{
    #                      webdriver:{
    #                        get: () => false
    #                      }
    #                    })
    #             }
    #         """)

    return page,browser





pull_down_new=""" async () => {
    await new Promise((resolve, reject) => {
        const maxScrollHeight = null
        const maxScrollTimes = null
        let currentScrollTimes = 0
        let scrollHeight = 0
        let maxTries = 5
        let tried = 0
        const timer = setInterval(() => {
            if (document.body.scrollHeight === scrollHeight) {
                tried += 1;
                if (tried >= maxTries) {
                    console.log("reached the end, now finished!")
                    clearInterval(timer)
                    resolve();
                }
            }
            scrollHeight = document.body.scrollHeight
            window.scrollTo(0, scrollHeight)
            window.scrollBy(0, -10)
            if (maxScrollTimes) {
                if (currentScrollTimes >= maxScrollTimes) {
                    clearInterval(timer);
                    resolve();
                }
            }
             if (maxScrollHeight) {
                if (scrollHeight >= maxScrollHeight) {
                    if (currentScrollTimes >= maxScrollTimes) {
                        clearInterval(timer);
                        resolve();
                    }
                }
            }
            currentScrollTimes += 1;
            // 还原 tried
            tried = 0
        }, 1000)
 
    })
}
"""


#无线下滑
pull_down="""
async () => {
    await new Promise((resolve, reject) => {
        // 允许下滑的最大高度，防止那种可以无限下拉的页面无法结束
        const maxScrollHeight = null;
        // 控制下拉次数
        const maxScrollTimes = null;
        let currentScrollTimes = 0;
        // 记录上一次scrollHeight，便于判断此次下拉操作有没有成功，从而提前结束下拉
        let scrollHeight = 0;
        // maxTries : 有时候无法下拉可能是网速的原因
        let maxTries = 5;
        let tried = 0;
        const timer = setInterval(() => {
            // 下拉失败，提前退出
            // BUG : 如果网速慢的话，这一步会成立~
            // 所以设置一个 maxTried 变量
            if (document.body.scrollHeight === scrollHeight) {
                tried += 1;
                if (tried >= maxTries) {
                    console.log("reached the end, now finished!");
                    clearInterval(timer);
                    resolve();
                }
            }
            scrollHeight = document.body.scrollHeight;
            window.scrollTo(0, scrollHeight);
            window.scrollBy(0, -10);
 
            // 判断是否设置了maxScrollTimes
            if (maxScrollTimes) {
                if (currentScrollTimes >= maxScrollTimes) {
                    clearInterval(timer);
                    resolve();
                }
            }
 
            // 判断是否设置了maxScrollHeight
            if (maxScrollHeight) {
                if (scrollHeight >= maxScrollHeight) {
                    if (currentScrollTimes >= maxScrollTimes) {
                        clearInterval(timer);
                        resolve();
                    }
                }
            }
            currentScrollTimes += 1;
            // 还原 tried
            tried = 0;
        }, 1000);
    });
};
"""
if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(pyppeteer_test("https://img0.bdstatic.com/static/searchresult/pkg/result_1676571.js"))
    #   asyncio.run(main())

