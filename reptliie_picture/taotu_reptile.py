#coding=utf-8
#!/usr/bin/python
# 导入requests库
import threading

import eventlet
import requests
# 导入文件操作库
import os
import bs4
from bs4 import BeautifulSoup
import sys
import importlib
import random
import time
import redis
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from concurrent.futures import ThreadPoolExecutor

importlib.reload(sys)
from selenium import webdriver

#套图爬取 和 分页爬取
# 越多越好
meizi_headers = [
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
# 给请求指定一个请求头来模拟chrome浏览器

global headers
headers = {'User-Agent': random.choice(meizi_headers)}
# 爬图地址
# mziTu = 'https://www.mzitu.com/'


mziTu = 'https://sc.chinaz.com/tupian/gudianmeinvtupian.html'
# 定义存储位置
global save_path
save_path = 'F:\BeautifulPictures'

Sum = 0  # 用于记录下载的图片数量



# 创建文件夹
def createFile(file_path):
    if os.path.exists(file_path) is False:
        os.makedirs(file_path)
    # 切换路径至上面创建的文件夹
    os.chdir(file_path)


# 下载文件
def download(page_no, file_path):
    global headers
    res_sub = requests.get(page_no, headers=headers)
    # 解析html
    soup_sub = BeautifulSoup(res_sub.text, 'html.parser')
    # 获取页面的栏目地址
    all_a = soup_sub.find('div',class_='postlist').find_all('a',target='_blank')
    count = 0
    for a in all_a:
        count = count + 1
        if (count % 2) == 0:
            headers = {'User-Agent': random.choice(meizi_headers)}
            print("内页第几页：" + str(count))
            # 提取href
            href = a.attrs['href']
            print("套图地址：" + href)
            res_sub_1 = requests.get(href, headers=headers)
            soup_sub_1 = BeautifulSoup(res_sub_1.text, 'html.parser')
            # ------ 这里最好使用异常处理 ------
            try:
                # 获取套图的最大数量
                pic_max = soup_sub_1.find('div', class_='pagenavi').find_all('span')[6].text
                print("套图数量：" + pic_max)
                for j in range(1, int(pic_max) + 1):
                    # 单位为秒，1-3 随机数
                    time.sleep(random.randint(1, 3))
                    headers = {'User-Agent': random.choice(meizi_headers)}
                    # print("子内页第几页：" + str(j))
                    # j int类型需要转字符串
                    href_sub = href + "/" + str(j)
                    print("图片地址："+href_sub)
                    res_sub_2 = requests.get(href_sub, headers=headers)
                    soup_sub_2 = BeautifulSoup(res_sub_2.text, "html.parser")
                    img = soup_sub_2.find('div', class_='main-image').find('img')
                    if isinstance(img, bs4.element.Tag):
                        # 提取src
                        url = img.attrs['src']
                        array = url.split('/')
                        file_name = array[len(array)-1]
                        # 防盗链加入Referer
                        headers = {'User-Agent': random.choice(meizi_headers), 'Referer': url}
                        img = requests.get(url, headers=headers)
                        print('开始保存图片', img)
                        f = open(file_name, 'ab')
                        f.write(img.content)
                        print(file_name, '图片保存成功！')
                        f.close()
            except Exception as e:
                print(e)


# 主方法
def main():
    total_taotu_dict=downloadimgSets()
    threadDownnload(total_taotu_dict)
    # num  = input("请输入要爬取的总页数:")
    # getPageimg(num)
    # res = requests.get(mziTu, headers=headers)
    # # 使用自带的html.parser解析
    # soup = BeautifulSoup(res.content, 'html.parser')
    # # 创建文件夹
    # createFile(save_path)
    # # 获取首页总页数
    # # img_max = soup.find('div', class_='nav-links').find_all('a')[3].text
    #
    # div = soup.find('div', {'class':  'tupian-list com-img-txt-list'})
    # if div is not None:
    #     links = div.find_all("div", attrs={'class': 'item'})
    #     for link in links:
    #         getimg(link)
    # else:
    #     print('Div not found')
    # print("总页数:"+img_max)
    # for i in range(1, int(img_max) + 1):
    #     # 获取每页的URL地址
    #     if i == 1:
    #         page = mziTu
    #     else:
    #         page = mziTu + 'page/' + str(i)
    #     file = save_path + '\\' + str(i)
    #     createFile(file)
    #     # 下载每页的图片
    #     print("套图页码：" + page)
    #     download(page, file)


def  getimg(link):
   if isinstance(link.find('img'), bs4.element.Tag):
               ##提取src
                img = 'https://sc.chinaz.com' + link.find('a').get('href')
                name = link.find('img').get('alt')
                #标签链接找到img标签
                url = link.find('img').attrs['src']
                array = url.split('/')
                file_name = array[len(array) - 1]
                names=file_name.split('.')
                name=name+'.'+names[1]
                # 创建子文件夹
                # createFile(save_path + '/' + name)
                # 判断相同文件夹下文件名是否相同名称
                file_name=existsFiles(save_path,name)
                # 防盗链加入Referer
                headers = {'User-Agent': random.choice(meizi_headers), 'Referer': url}
                img=getimg2(img)
                global Sum
                Sum+=1
                img = requests.get(img, headers=headers)
                print('开始保存图片', img)
                f = open(file_name, 'ab')
                f.write(img.content)
                print(file_name, '图片保存成功！')
                f.close()

def  file_name_check(file_name):
    temp_file_name =file_name
    i=1
    while i:
        print(temp_file_name)
        children_path=save_path + '/' + temp_file_name
        print(os.path.exists(children_path))
        if os.path.exists(children_path):
            #先对file_name进行截取
            name, suffix = file_name.split('.')
            if i!=1:
               name += '(' + str(i) + ')'
            else:
               name=name
            temp_file_name = name + '.' + suffix
            i += 1
        else:
            return temp_file_name

def file_name_check2(fileName):
        name, suffix = fileName.split('.')
        # 创建 Redis 客户端对象
        r = redis.Redis(host='localhost', port=6379, db=0)
        #判断key是否存在
        if r.exists('path:'+fileName):
            count = int(r.get('path:'+fileName))
            count += 1
            name += '(' + str(count) + ')'
            fileName = name + '.' + suffix
            r.incr('path:'+fileName)
        else:
            # 对键进行自增操作
            r.incr('path:'+fileName)
            # 对键进行指定增量的自增操作
            # r.incrby('count', 1)
        return fileName


def   existsFiles(path,fileName):
    file_names = os.listdir(path)
    if contains_char(fileName,file_names):
        fileName= file_name_check2(fileName)
    return fileName

def contains_char(char, lst):
  for item in lst:
    if item == char:
     return True
  return False

def getimg2(url):
    res = requests.get(url, headers=headers)
    # 使用自带的html.parser解析
    soup = BeautifulSoup(res.content, 'html.parser')
    soup_sub=soup.find('div',{'class':  'img-box'})
    links=soup_sub.find_all('img')
    for link in links:
         imgurl = 'https:'+link.get('src')
    return imgurl


def downloadimg(num):
    global mziTu
    if num != 1:  # 第一页特殊处理
        mziTu = 'https://sc.chinaz.com/tupian/gudianmeinvtupian_'+str(num)+'.html'  # 图片地址
    res = requests.get(mziTu, headers=headers)
    # 使用自带的html.parser解析
    soup = BeautifulSoup(res.content, 'html.parser')
    # 创建文件夹
    createFile(save_path)
    # 获取首页总页数
    # img_max = soup.find('div', class_='nav-links').find_all('a')[3].text
    div = soup.find('div', {'class': 'tupian-list com-img-txt-list'})
    if div is not None:
        links = div.find_all("div", attrs={'class': 'item'})
        for link in links:
            getimg(link)
    else:
        print('Div not found')


def  getPageimg(num):
        for i in range(1, int(num) + 1):
            downloadimg(i)
            print(f"第{i}页爬取完成")
            print(f"共下载{Sum}张图片")



#----------------------------动态页面加载爬取-----------------------------
taotu_path1 = 'https://taotu123.com'
save_path1="F:\BeautifulPictures/taotu1/"
# (2) 创建浏览器操作对象，就是指定我们驱动的路径
path = 'D:\chromDriver\chromedriver-win64\chromedriver.exe'

#创建套图字典
taotu_dict={}
global total_taotu_dict
total_taotu_dict={}

def  downloadimgSets():
    num  = input("请输入要加载的次数:")
    browser = webdriver.Chrome()
    browser.maximize_window()
    browser.implicitly_wait(6)
    browser.get(taotu_path1)
    r = redis.Redis(host='localhost', port=6379, db=0)
    for i in range(1,int(num)+1):
        index_taotu_dict={}
        if i!=1:
            time.sleep(5)
            button = browser.find_element(By.CLASS_NAME, "view-more-button")
            button.click()
        iterationImg(browser,r,index_taotu_dict)
        total_taotu_dict.update(index_taotu_dict)
    return total_taotu_dict

    # content = browser.page_source
    # soup = BeautifulSoup(content, 'html.parser')
    # div=soup.find("ul",{'id': 'post_list_box'})
    # links = div.find_all("div", attrs={'class': 'list-content d-flex flex-column flex-fill'})
    # total_size = len(links)
    #
    # for link in links:
    #    url= link.find('a').get('href')
    #    name=link.find('a').get_text()
    #
    # button = browser.find_element(By.CLASS_NAME,"view-more-button")
    # button.click()



def  iterationImg(browser,r,total_taotu_dict):
    content = browser.page_source
    soup = BeautifulSoup(content, 'html.parser')
    div = soup.find("ul", {'id': 'post_list_box'})
    links = div.find_all("div", attrs={'class': 'list-content d-flex flex-column flex-fill'})
    total_size = len(links)
    #总数量一定要比当前下标数量大
    if r.exists('index'):
        index_size=int(r.get('index'))
        r.set('index', total_size)
    else:
        index_size=0;
        r.set('index', total_size)
    for i in range(index_size,total_size):
        url=links[i].find('a').get('href')
        url=taotu_path1+url;
        name = str(links[i].find('a').get_text()).replace(" ","")
         #H获取套图
        downnloadimg3(url,name,total_taotu_dict)
        print(url+"["+name+"]")
    print(total_taotu_dict)


def  downnloadimg3(url,name,total_taotu_dict):
      # 防盗链加入Referer
      getimg3(url,name,total_taotu_dict)
      #保存下载
      # downloadForImage(total_taotu_dict)

#返回所有url和name集合
def getimg3(url,name,total_taotu_dict):
    headers = {'User-Agent': random.choice(meizi_headers), 'Referer': url}
    res = requests.get(url, headers=headers)
    # 使用自带的html.parser解析
    soup = BeautifulSoup(res.content, 'html.parser')
    soup_sub=soup.find('div',{'class':  'row fdbox'})
    links=soup_sub.find_all('img')
    taotu_dict={}
    for i in range(0,len(links)):
         global Sum
         Sum += 1
         imgurl =links[i].get('src')
         urls=imgurl.split('.')
         end=urls[-1]
         numbers=str(i)
         urlname=str(name+numbers+'.'+end)
         if urls[-1] == 'jpg' or urls[-1] =='png':
             taotu_dict[urlname]=imgurl
    total_taotu_dict[name]=taotu_dict



count = 20

#动态爬取相应的url
def downloadForImage(item):
    for name, values in item.items():
        createFile(save_path1 + name)
        for key, value in values.items():
            # eventlet.monkey_patch()  # 必须加这条代码
            # with eventlet.Timeout(20, False):
                # time.sleep(21)
                key=str(key).replace("/","")
                img = requests.get(value, headers=headers,timeout=count)
                print('开始保存图片', img)
                f = open(save_path1+name+'/'+key, 'ab')
                f.write(img.content)
                print(key, '图片保存成功！')
                f.close()




#
# def task():
#     downloadimgSets()
#
# thread_pool = ThreadPoolExecutor(max_workers=20)
# thread_pool.submit(task)
# thread_pool.shutdown()

def threadDownnload(big_dict):
    sub_dicts = split_dict_by_count(big_dict, count)

    threads = []
    for sub_list in sub_dicts:
        t = threading.Thread(target=downloadForImage, args=(sub_list,))
        threads.append(t)
        t.start()

    # 等待所有线程执行完毕
    for t in threads:
        t.join()

def split_dict_by_count(dictionary, count):
    sub_dicts = []
    keys = list(dictionary.keys())
    total_keys = len(keys)

    for i in range(0, total_keys, count):
        sub_dict = {k: dictionary[k] for k in keys[i:i + count]}
        sub_dicts.append(sub_dict)

    return sub_dicts

if __name__ == '__main__':
    main()
   # task()