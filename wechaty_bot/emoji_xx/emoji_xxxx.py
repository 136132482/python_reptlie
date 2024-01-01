import asyncio
import os
import random
import time
import uuid

from bs4 import BeautifulSoup
from syncer import sync
from comment import pyppeteer_demo,comment_util
import requests
import pytesseract
from PIL import Image
import easyocr
import cv2
import paddlehub as hub
import PIL.ImageOps
import  re
from faker import Faker

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

class  emoji_xxxx(object):
    async def save_pic(self,url,name):
        img = requests.get(url, headers=headers)
        type=requests.head(url).headers['Content-Type']
        type=type.split("/")[1]
        name=name+"."+type
        print('开始保存图片', img)
        comment_util.createFile(save_path)
        file_name=os.path.join(save_path,name)
        f = open(file_name, 'ab')
        f.write(img.content)
        print(file_name, '图片保存成功！')
        f.close()





    async def  get_emoji(self,emoji_path):
        page,browser=await pyppeteer_demo.pyppeteer_test(emoji_path)
        await  page.evaluate("""()=>{
                var element = document.querySelector('.MuiPaper-root MuiDialog-paper MuiDialog-paperScrollPaper MuiDialog-paperWidthSm MuiPaper-elevation24 MuiPaper-rounded')
                element=element[0]
                if (element && element.getAttribute('role') === 'dialog') {
                element.parentNode.removeChild(element);
              }              
        }""")
        # await page.setRequestInterception(True)
        # page.on('request', pyppeteer_demo.intercept_request)
        # page.on('response', pyppeteer_demo.intercept_response)
        # await self.get_winodws_scroll(page)
        i = 0
        while i < 30:
            await asyncio.sleep(3)
            if i>0:
                ele=await page.xpath('//*[@id="root"]/div[1]/header/div/div[1]/div/div/input')
                ele=ele[0]
                await ele.focus()
                # await ele.keyboard.down('Backspace')
                # await page.focus("input[type='text']")
                await page.keyboard.down('Backspace')
                await page.type("input[type='text']",str(i))
                ele= await  page.xpath("//*[@id='root']/div[1]/header/div/div[1]/div/button")
                ele=ele[0]
                await ele.click()
            else:
              await page.type("input[id='searchInput']", str(i))
              await page.click("button[class='jss15']")
            await asyncio.sleep(2)
            # await page.evaluate
            page = (await browser.pages())[-1]
            await page.setRequestInterception(True)
            page.on('request', pyppeteer_demo.intercept_request)
            page.on('response', pyppeteer_demo.intercept_response)
            await self.get_winodws_scroll(page)
            await page.evaluate("()=>{document.documentElement.scrollTop=0}")
            i += 1
        await browser.close()


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



    async def get_winodws_scroll(self,page):
        # 获取当前页面的高度
        last_height = await page.evaluate("()=>{return document.body.scrollHeight}")
        # 模拟下拉操作，直到滑动到底部
        while True:
            # 模拟下拉操作
            await page.evaluate("""()=>{
            window.scrollTo(0, document.body.scrollHeight)
            }
            """)
            # 等待页面加载
            await asyncio.sleep(2)
            # 获取当前页面的高度
            new_height =await page.evaluate("()=>{return document.body.scrollHeight}")
            # 判断是否已经到达页面底部
            if new_height == last_height:
                break
            # 继续下拉操作
            last_height = new_height

     #准备率稍微有点低 需要进行图像黑白化 提高分辨率
    def  tessercat_read(self,save_path):
        for file in os.listdir(save_path):
            if not comment_util.has_chinese(file):
                path = os.path.join(save_path, file)
                try:
                    image=cv2.imread(path, cv2.IMREAD_GRAYSCALE)
                    # gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)#灰度
                    # --psm 7 单行识别 , --oem 3 使用 LSTM OCR 引擎 , -c tessedit_char_whitelist=0123456789 只识别数字字符
                    config = "--psm 7 --oem 3 -c tessedit_char_whitelist=0123456789"
                    text = pytesseract.image_to_string(image,config=config, lang='chi_sim')
                    # text = ''.join(re.findall('\d+', text))
                    content=comment_util.remove_special_characters(text)
                    if content != '':
                        format = file.split(".")[1]
                        text = content + "." + format
                        new_path = os.path.join(save_path, text)
                        if os.path.exists(path):
                            # fake = Faker(["zh_CN"])
                            text=content+str(random.randint(0,10000))+"."+format
                            new_path=os.path.join(save_path,text)
                        # comment_util.createFile(new_save_path)
                        # cv2.imwrite(new_path,image)
                        os.rename(path,new_path)
                        print("重命名成功：" + text)
                except Exception as e:
                    print(e)
                    # os.remove(path)


    def update_image(self):
        return



    async def read_img(self,list_file):
        for file in list_file:
            path=os.path.join(save_path, file)
            # im = Image.open(path)
            # string = pytesseract.image_to_string(im, lang='chi_sim')
            try:
                ocr = hub.Module(name="chinese_ocr_db_crnn_server", enable_mkldnn=True)
                image = cv2.imread(path)
                # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                ocr_result = ocr.recognize_text(images=[image])
                text_list = []
                for i in ocr_result[0]["data"]:
                    text=i['text']
                    text_list.append(text)
                text="".join(text_list)
                text=comment_util.remove_special_characters(text)
                if text!='':
                    format=file.split(".")[1]
                    text=text+"."+format
                    new_path = os.path.join(save_path, text)
                    os.rename(path,new_path)
                    print("重命名成功："+text)
            except Exception as e:
                 print(e)
                 os.remove(path)
                # reader = easyocr.Reader(['ch_sim'])
                # result = await reader.readtext(path, detail=0, paragraph=True)
                # print(result)
                # print(string)





if __name__=="__main__":
    emoji=emoji_xxxx()
    asyncio.get_event_loop().run_until_complete(emoji.get_emoji("http://www.dbbqb.com/"))
    # list = os.listdir(save_path)
    # asyncio.get_event_loop().run_until_complete(comment_util.threadDownnloadNoarg_async(list,emoji,'read_img'))
    # emoji.tessercat_read(save_path)
    # asyncio.get_event_loop().run_until_complete(emoji.read_img(list))
    # tessercat_read()