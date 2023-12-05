import asyncio
import concurrent
import json
import operator
import time

import requests
from Crypto.Cipher import AES
import base64
import binascii
import os
from bs4 import BeautifulSoup
from tqdm.asyncio import tqdm_asyncio, trange

from reptliie_picture import taotu_reptile
from reptlie_book import  book
from browsermobproxy import Server

from reptlie_video import dict_video

from re import search

# 经postman调用，发现这个网站请求需要请求头，否则会返回资源禁止访问
headers = {
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
}
# key = requests.get(key_url, headers = headers).content
save_ts_path='F:\\Video\\ts_video'

video_path="https://087a.wlfnnu.com"


import os
import requests
import random
from multiprocessing.pool import ThreadPool
from tqdm import tqdm





async def get_downts(list_ts,videoName,key,iv):
    print('开始下载')
    downnname = os.path.join(save_ts_path, videoName)
    taotu_reptile.createFile(downnname)
    # 下载ts文件  video-0000.ts   video-0213.ts
    for i in trange(0, len(list_ts)):
       try:
        ts_url=list_ts[i]
        name=os.path.basename(ts_url)
        name=name.split("?")
        res_ts = requests.get(ts_url).content
        # 下载的 video-0000.ts video-0213.ts 文件保存目录
        video_path=downnname + "/" + name[0]
        if os.path.exists(video_path):
            continue
        with open(video_path,'wb') as ts:
            # 解密
            #binascii.a2b_hex('f366f6408751d3c81696382ea0a89113')
            cryptor = AES.new(key, AES.MODE_CBC,binascii.a2b_hex(iv[2:]))
            ts.write(cryptor.decrypt(res_ts))
            print('下载:' + downnname)
       except Exception as e:
           print("iv="+iv+",videoName="+videoName+"ts_url="+ts_url)
           print(e)
    print('下载完成')
    await mergeMp4(downnname)
    await removets(downnname)
    return downnname

async def  mergeMp4(downnname):
    mp4path=os.path.join(downnname,"mp4")
    taotu_reptile.createFile(mp4path)
    cmd = f'copy /b {downnname}\\*.ts {mp4path}\\my.ts'
    os.chmod(downnname, 0o755)
    os.system(cmd)
    cmd=f'ffmpeg -y -i {mp4path}\\my.ts  -c  copy {mp4path}\\my.mp4'
    os.system(cmd)

async def  removets(downnname):
    files=os.listdir(downnname)
    for file in files:
       if os.path.isfile(os.path.join(downnname,file)):
           os.remove(os.path.join(downnname,file))

def  get_content(url):
    contents = requests.get(url).text
    # output = str(content, 'UTF-8')
    contents=contents.split("\n")
    list_ts=[]
    list_video_ts={}
    if contents[0] != "#EXTM3U":
        raise BaseException(u"非M3U8的链接")
    for line in contents:
       if line.startswith('https://'):
           list_ts.append(line)
       if "#EXT-X-KEY" in line:
           url_http = line[line.find("URI"):line.rfind('"')].split('"')[1]
           iv = line[line.find("IV"):].split(',')[0].split('=')[1]
           key=get_key(url_http)
           list_video_ts['iv']=iv
           list_video_ts['key']=key
    list_video_ts['ts']=list_ts
    return list_video_ts

def get_key(url):
   key = requests.get(url).content
   return key

num = 1
list_video = {}
def get_network(path):
   global list_video
   video_list=[]
   bf=None
   for i in range(0,num):
       bf=book.get_soup(path)
       video_list_index=bf.find("div",attrs={"class":"video-list"}).find_all("div",attrs={"class":"video-item"})
       video_list.extend(video_list_index)

   [get_video_item(video_item) for video_item  in video_list]
   with concurrent.futures.ThreadPoolExecutor() as exectuor:
       for video_name,video_url in  list_video.items():
           future =exectuor.submit(get_href_video,video_url)
           if len(future.result())!=0:
             if type(future.result())==list:
               list_video[video_name]=future.result()
       exectuor.shutdown(wait=True)

   get_showList()
   video_list.clear()
   return bf


def get_showList():
    # sub_list_video={}
    # for key,value in list_video.items():
    #       if type(value)==list:
    #           sub_list_video[key]=value
    print(list_video)
    keys = list(list_video.keys())
    if len(keys) == 0:
        print("\n当前页面没有视频")
        os._exit()
    [print("(" + str(i) + ")" + keys[i]) for i in range(0, len(keys))]




def get_href_video(video_url):
    brower = book.click(video_path+video_url)
    time.sleep(2)
    network = brower.execute_script("return window.performance.getEntries();")
    brower.close()
    list_m3u8 = []
    list_videos=[]
    for data in network:
        if data['name'].startswith("https://") :
           # if operator.contains(data['name'],'auth_key'):
              # print(data["name"])
              if '.m3u8' in data['name']:
                  list_m3u8.append(data['name'])
                  print("这个是key:"+data['name'])
              # if operator.contains(data['name'], '.ts'):
              #     print("这个是ts:" +data['name'])
    for   m3u8 in  list_m3u8:
        list_video_ts=get_content(m3u8)
        if len(list_video_ts) !=0:
          list_videos.append(list_video_ts)

    return   list_videos
        # if data.get('initiatorType') is None:
        #     continue
        #
        # if data["initiatorType"]=='xmlhttprequest':
        #
        #     print(data["name"])



def get_video_item(video_item):
     video_url= video_item.find("a").get("href")
     video_name=video_item.find("div",attrs={"class","title"}).get_text()
     list_video[video_name]=video_url


async def get_list_video_download():
     # list_video=dict_video.dict_video
     print(list_video)
     task_list_all=[]
     for  videoname, values  in list_video.items():
         if type(values) !=list:
             continue
         if len(values)>0:
             videoname=book.remove_special_characters(videoname)
             task_list=await get_video_download(videoname,values)
             task_list_all.extend(task_list)

     done = await tqdm_asyncio.gather(*task_list_all, timeout=None)
     for done_task in done:
         print(str(done_task) + "执行完毕\n\n")

async def  get_video_download(videoname,values):
        task_list=[]
        for i in range(0,len(values)):
            list_ts=values[i]['ts']
            iv=values[i]['iv']
            key=values[i]['key']
            task=await asyncio.create_task(get_downts(list_ts,videoname+"(+"+str(i)+")",key,iv))
            task_list.append(task)
            # get_downts(list_ts, videoname, key, iv)
        return task_list


def  downloadcurrent(path):
    get_choice_num()
    bf=get_network(path)

    #下载当前页所有ts
    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_list_video_download())

    get_click_page(bf)
    list_video.clear()



choice_flag=True
def get_choice_num():
        global num
        global choice_flag
        while choice_flag:
            try:
                nums = int(input("请选择下载当前页，还是自定义数字进行下载 1：一页一页下  2：自定义数字页数进行下载"))
                if nums == 1:
                    num=1
                    choice_flag=False
                    break
                elif nums == 2:
                    nums = int(input("请输入自定义页数数字进行下载"))
                    num=nums
                    choice_flag=False
                    break
                else:
                    raise
            except Exception as e:
                print(e)
                print("你输入的不正确，请重新输入")


async def get_click_page(bf):
        while True:
            try:
                num=int(input("请确认是否进行继续下载，1：是 2：退出  (继续下载会按照你最初选择的定义页数继续进行)"))
                if num ==1:
                    next_page_url=bf.find("a",attrs={"class","next cursor-pointer iconfont icon-arrow-down"}).get("href")
                    path=os.path.join(video_path, next_page_url)
                    downloadcurrent(path)
                    break
                else:
                    os._exit(0)
                    break
            except Exception as e:
                print(e)
                print("你输入的不正确，请重新输入")



if __name__ == '__main__':
    # list_ts = get_content("https://hls.vdtuzv.com/videos3/25706b7b99d864158c4a607c96dc94eb/25706b7b99d864158c4a607c96dc94eb.m3u8")
    # get_downts(list_ts,"111","https://tp1.panqing80.club/videos3/25706b7b99d864158c4a607c96dc94eb/crypt.key?auth_key=1701656443-6-0-fded7d7a4a60b0e24bd83abe8115a3dd")
    # print(list_ts)
    #获取当前页
    # get_network()
    # #下载当前页所有ts
    # downloadcurrent(video_path)

    # mergeMp4("F:\Video\\ts_video\\疯马秀真的脱了")
    # removets("F:\Video\\ts_video\\疯马秀真的脱了")

    downloadcurrent("https://087a.wlfnnu.com/category/7/2.html")



