# 导入requests库
import threading

import requests
# 导入文件操作库
import codecs
import os
from bs4 import BeautifulSoup
import sys
import importlib

from tqdm import tqdm, trange

from dynamic_database import test1
from dynamic_database import test2
from dynamic_database  import mysql_DBUtils
from reptlie_book import briefs_dict

importlib.reload(sys)
import httpx
import random
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
import time
import colorsys
import concurrent.futures
import progressbar
import re


#驱动放在reptlie_book目录下
service = ChromeService(executable_path='D:\chromDriver\chromedriver-win64/chromedriver.exe')

mysql = mysql_DBUtils.MyPymysqlPool("dbMysql1")

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

# proxies = ['HTTP://110.243.30.23:9999', 'HTTP://222.189.191.206:9999', 'HTTP://118.212.104.138:9999',
#            'HTTP://182.149.83.97:9999', 'HTTP://106.42.163.100:9999', 'HTTP://120.83.107.69:9999',
#            'HTTP://60.13.42.135:9999', 'HTTP://60.205.188.24:3128', 'HTTP://113.195.232.23:9999',
#            'HTTP://59.62.36.74:9000', 'HTTP://218.2.226.42:80']
# proxy = {'HTTP': random.choice(proxies)}

num=1
num1=1
num2=1
headers = {'User-Agent': random.choice(headers)}
# headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'}
server = 'https://wap.ibiquges.org'
# 星辰变地址
book = f'https://wap.ibiquges.org/wapfull/{num}.html'
#分类book
typebook=f'https://wap.ibiquges.org/wapsort/{num1}+"_"+{num2}'
#完本book
wapbook=f'https://wap.ibiquges.org/wapfull/{num}.html'
# 定义存储位置
global save_path
save_path = 'F:\Book'
if os.path.exists(save_path) is False:
    os.makedirs(save_path)


def click(click_url):
    browser = webdriver.Chrome(service=service)
    browser.maximize_window()
    browser.implicitly_wait(6)
    browser.get(click_url)
    return browser

#获取html
def get_soup(url):
    res = httpx.get(url, headers=headers, timeout=10, verify=False)
    html = res.content
    html_doc = str(html, 'utf8')
    bf = BeautifulSoup(html_doc, 'html.parser')
    return bf



# 获取章节内容
def get_contents(chapter,texts_content):
    bf=get_soup(chapter)
    texts = bf.find('div', attrs={'id':'nr1'}).get_text()
    texts_content.append(texts)
    link= bf.find("td",attrs={'class':'next'}).find('a')
    if link.get_text() =='下一页':
        pageurl = server +link.get('href')
        get_contents(pageurl,texts_content)
    # 获取div标签id属性content的内容 \xa0 是不间断空白符 &nbsp;

def get_texts_content(chapter):
    texts_content = []
    get_contents(chapter,texts_content)
    texts="\n".join(texts_content)
    content = texts.replace('\xa0' * 4, '\n').replace("最新网址：wap.ibiquges.org","")+"\n"
    texts_content.clear()
    return content



def get_contentsClick(chapter):
    global texts_content
    brower=click(chapter)
    get_text(brower)
    brower.close()
    # 获取div标签id属性content的内容 \xa0 是不间断空白符 &nbsp;
    texts="\n".join(texts_content)
    content = texts.replace('\xa0' * 4, '\n').replace("最新网址：wap.ibiquges.org","")+"\n"
    texts_content.clear()
    return content


def  get_text(brower):
        brower.find_element(By.CLASS_NAME,"next").click()
        bf = BeautifulSoup(brower.page_source, 'html.parser')
        texts = bf.find('div', attrs={'id': 'nr1'}).get_text()
        texts_content.append(texts)
        link = bf.find("td", attrs={'class': 'next'}).find('a')
        if link.get_text() == '下一页':
            get_text(brower)



# 写入文件
def write_txt(chapter, content, code):
    with codecs.open(chapter, 'a', encoding=code)as f:
        f.write(content)

def write_txtw(chapter, content, code):
    with codecs.open(chapter, 'w', encoding=code)as f:
        f.write(content)
# 主方法
def main():
    soup = get_soup(book)
    # 获取所有的章节
    a = soup.find('div', attrs={'class':'cover'}).find_all('a')
    print('总章节数: %d ' % len(a))
    for each in a:
        try:
            chapterurl = server + each.get('href')
            waphtml(chapterurl,each.get_text())
        except Exception as e:
            print(e)


#数据库字典
total_briefs_dict = {}
#获取当前小说完本页面的所有内容
def  waphtml(chapterurl,bookname):
    section_urls={}
    browser=click(chapterurl)
    soup=BeautifulSoup(browser.page_source,'html.parser')
    # soup= get_soup(chapterurl)
    #X先要把书的作者，分类，状态 更新时间，最新章节  书的名称
    ps=soup.find("div",attrs={'class':'block_txt2'}).find_all('p')
    book_info=soup.find("div",attrs={'class':'intro_info'}).get_text()
    book_img=soup.find("div",attrs={'class':'block_img2'}).find("img").get("src")
    briefs=[p.get_text() for p in  ps if len(p.get_text())]
    briefs_dict={}
    briefs_dict['书名']= bookname.strip().split("\n")[0]
    briefs_dict['简介']=book_info
    briefs_dict['图片']=book_img
    briefs_dict['图书下载链接']=chapterurl
    for b  in briefs :
      b=b.split("：")
      if len(b)>1:
        briefs_dict[b[0].strip()] = b[1].strip()
    #找章节
    # links = soup.find('div', attrs={'class': 'cover'}).find_all("li")
    iterationChapterClick(soup,browser,section_urls,True)
    briefs_dict['章节url']=section_urls
    total_briefs_dict[bookname] = briefs_dict


#Z这个主要是下载
def  saveSectionUrl(links,section_urls):
    for each in links:
        try:
            chapter = server + each.find('a').get('href')
            chapterName = each.get_text()
            #这个主要存储在数据库里面
            section_urls[chapterName] = chapter
            # 下载
            # downnloadBook(chapter, bookname)
        except Exception as e:
            print(e)



#soup 第一章节soup
def  iterationChapterClick(soup,browser,section_urls,flag):
    start = time.time()
    while flag:
      try:
            links = soup.find('div', attrs={'class': 'cover'}).find_all("ul")
            links = links[1].find_all('li')
            saveSectionUrl(links,section_urls)
            chapter = soup.find("span", attrs={'class': 'right'}).find('a').get('href')
            if chapter is None:
                flag=False
                break
            browser.find_element(By.CLASS_NAME,"right").click()
            content=browser.page_source
            soup = BeautifulSoup(content, 'html.parser')
            iterationChapterClick(soup,browser,section_urls,flag)
      except Exception as e:
          print(e)
      return
    end = time.time()
    print("共计耗时" + str(end - start))



def  iterationChapter(soup,section_urls):
    start=time.time()
    while True:
        try:
            links = soup.find('div', attrs={'class': 'cover'}).find_all("ul")
            links=links[1].find_all('li')
            saveSectionUrl(links,section_urls)
            chapter = soup.find("span", attrs={'class': 'right'}).find('a').get('href')
            if chapter is None:
               break
            else:
                soup = get_soup(server + chapter)
                iterationChapter(soup,section_urls)
        except Exception as e:
            print(e)
        return
    end =time.time()
    print("共计耗时"+str(end-start))

def downnloadBook(chapterName,chapter,bookname,pbar):
    content = get_texts_content(chapter)
    chapter = save_path + "/" + bookname+ ".txt"
    write_txt(chapter, content, 'utf8')
    print("\n ["+bookname+"]"+"当前下载章节为:"+chapterName+'下载完成')
    pbar.update(1)

def downnloadBooksubChapter(chapterBeans,pabr):
    for i in trange(len(chapterBeans)):
        chapterNameId = chapterBeans[i].get('id')
        chapterName=chapterBeans[i].get('章节名称')
        chapterName=remove_special_characters(chapterName)
        chapterName=str(chapterNameId)+chapterName
        chapter= chapterBeans[i].get('章节url')
        bookname=chapterBeans[i].get('书名')
        content = get_texts_content(chapter)
        chapter = os.path.join(save_path,bookname,chapterName+".txt")
        # if os.path.exists(chapter):
        #      print("该章节已下载："+ chapter)
        # chapter = save_path + "/" + bookname+"/"+chapterName+ ".txt"
        write_txtw(chapter, content, 'utf8')
        print("\n ["+bookname+"]"+"当前下载章节为:"+chapterName+'下载完成')
        pabr.update(1)
def remove_special_characters(string):
    string=string.replace(" ","")
    string = string.replace("/", "")
    string = string.replace("?", "")
    string = string.replace("\"", "")
    string = string.replace("！", "")
    string = string.replace("！", "")
    string = string.translate(str.maketrans('', '', '@#$%^&*()_+'))
    return string


def thread_downloadBook(sub_list,bookname):
    p = progressbar.ProgressBar()
    # for key,value in sub_list.items():
    lock.acquire()
    for i in  p(range(0,len(sub_list))):
        key=list(sub_list.keys())[i]
        value = list(sub_list.values())[i]
        downnloadBook(key,value,bookname)
    lock.release()



sub_links=[]
#第一步 搜索功能
def  searchBook(click_url,links):
    serach_key=input("请输入你要查找的书籍\n")
    browser=click(click_url)
    browser.find_element(By.NAME,"searchkey").send_keys(serach_key)
    browser.find_element(By.NAME, "submit").send_keys(serach_key)
    browser.find_element(By.NAME, 'submit').click()
    content = browser.page_source
    soup = BeautifulSoup(content, 'html.parser')
    browser.close()
    links = soup.find('div', attrs={'class': 'read_book'}).find_all('div',attrs={'class':'block_txt'})
    [print("({})".format(i)+links[i].get_text()) for i in range(0,len(links))]
    sub_links=get_true(click_url,links)
    return sub_links


def  get_true(click_url,links):
    global sub_links
    while True:
        try:
            nums = input("请输入你想下载的书籍数字(可多选,以逗号隔开,不选取数字直接enter确认默认下载所有,重新查找请输入#号建)\n")
            if nums is None or nums =='':
              sub_links=links
              break
            elif nums =='#' or  len(links)==0:
               searchBook(click_url,sub_links)
               break
            else:
              list_nums = nums.split(",")
              sub_links=[ links[int(num)] for num in list_nums]
              break
        except Exception as e :
            print(e)
            print("你输入的不正确，请重新输入")
    return  sub_links



lock=threading.Lock()
# 主要是用于这个书籍列表的目录
def getBookList(links):
   with concurrent.futures.ThreadPoolExecutor() as exectuor:
     for i in range(0,len(links)):
       exectuor.submit(process_book,links[i])
   exectuor.shutdown(wait=True)

def process_book(link):
    str = link.find_all('a')[0].get('href')
    chapter = server + str
    bookname = link.get_text()
    waphtml(chapter, bookname)


thread_count=2000
def foreachDownload():
    with concurrent.futures.ThreadPoolExecutor() as exectuor:
        for i in range(0,len(list(total_briefs_dict.keys()))):
            bookname= list(total_briefs_dict.keys())[i]
            values = list(total_briefs_dict.values())[i]
            exectuor.submit(thread_submit,values,bookname)
    exectuor.shutdown(wait=True)


def  thread_submit(values,bookname):
        section_urls = values['章节url']
        bookname = bookname.strip().split("\n")
        with tqdm(total=len(section_urls)) as pbar:
            for i in range(0, len(section_urls)):
                key = list(section_urls.keys())[i]
                value = list(section_urls.values())[i]
                downnloadBook(key, value, bookname[0],pbar)

            #下载本地暂时不用多线程
        # threadDownnload(section_urls,bookname[0])



#bookname 书名 section_urls 所有章节url 这个用字典干
def threadDownnload(datas,bookname):
    sub_chapters = split_dict_by_book(datas, thread_count)
    threads = []
    for sub_list in sub_chapters:
        print(sub_list)
        t = threading.Thread(target=thread_downloadBook, args=(sub_list,bookname))
        threads.append(t)
        t.start()

    # 等待所有线程执行完毕
    for t in threads:
        t.join()



def split_dict_by_book(datas, count):
    sub_chapters = []
    keys = list(datas.keys())
    total_keys = len(keys)

    for i in range(0, total_keys, count):
        sub_chapter = {k: datas[k] for k in keys[i:i + count]}
        sub_chapters.append(sub_chapter)
    return sub_chapters




#自定义穿创建表
def createtabl(tableName):
    #测试数据
    # total_briefs_dict=briefs_dict.total_briefs_dict
    insert_datas=[]
    for bookname, values in total_briefs_dict.items():
        columns = []
        fild_value = []
        for key,value in values.items():
           column = {}
           if key!='章节url':
               column['column_name']=key
               if key=='简介':
                column['column_definition']='TEXT'
               else:
                column['column_definition'] = 'VARCHAR(100)'
               column['column_isornot'] = 1
               columns.append(column)
               if key=='书名':
                   value = value.strip().split("\n")[0]
               fild_value.append(value)
        insert_datas.append(tuple(fild_value))
    #主要问题点 这里不需要循环判断
    test1.createTable(tableName,columns)
    exists_index(tableName, 'index_name_author','书名','作者')
    save_datas(tableName,columns, insert_datas,'书名','作者')



# #数据库保存
def save_datas(tableName,columns,insert_datas,name1,name2):
    test2.beansFieldtoPackage(tableName)
    test2.packageList(tableName,columns,insert_datas,name1,name2)




def  svae_dataurls(tableName,tableName1):
    columns_url = []
    # total_briefs_dict = briefs_dict.total_briefs_dict
    column1 = {}
    column1['column_name'] = '章节名称'
    column1['column_definition'] = 'varchar(100)'
    column1['column_isornot'] = 1
    column2 = {}
    column2['column_name'] ='章节url'
    column2['column_definition'] = 'varchar(100)'
    column2['column_isornot'] = 1
    column3 = {}
    column3['column_name'] = 'reptlie_book_id'
    column3['column_definition'] = 'int'
    column3['column_isornot'] = 1
    columns_url.append(column1)
    columns_url.append(column2)
    columns_url.append(column3)

    fild_url_values = []
    for bookname, values in total_briefs_dict.items():
         section_urls = values['章节url']
         bookname = values['书名']
         bookname = bookname.strip().split("\n")[0]
         author = values['作者']
         sql = f"select id from {tableName} where  书名 = '%s' and 作者 = '%s' " % (bookname, author)
         res = test1.queryone(sql)
         if res is False:
             raise ValueError("该书以删除~！")
         for key,value in section_urls.items():
             fild_url_value = (key,value,res[0])
             fild_url_values.append(fild_url_value)
    print(fild_url_values)
    test1.createTable(tableName1, columns_url)
    exists_index(tableName1, 'index_url_name','章节url','章节名称')
    save_datas(tableName1,columns_url, fild_url_values,'章节url','章节名称')

def exists_index(tableName,index_name,bookname,author):
    show_sql=f"SHOW INDEX FROM {tableName} WHERE Key_name = '{index_name}' "
    res=mysql.getOne(show_sql)
    print(res)
    if res  is False:
        index_sql=f"ALTER table {tableName} add  UNIQUE index {index_name}({bookname},{author})"
        mysql.insert(index_sql)



def  choice_downnormysql():
    while True:
        try:
            nums = input("请选择数字 1:下载到本地 2：下载到数据库")
            if nums =='1':
                # 下载
                foreachDownload()
                break
            elif nums=='2':
                # 下载到数据库
                tablename = 'reptlie_book'
                createtabl(tablename)
                tablename1 = 'reptlie_book_url'
                svae_dataurls(tablename, tablename1)
                break
            else:
                raise
        except Exception as e :
            print(e)
            print("你输入的不正确，请重新输入")

def a_connected_sequence():
    links=searchBook(server,None)
    getBookList(links)
    print(total_briefs_dict)
    choice_downnormysql()




def   voluntarily():
    # links=searchBook(server,None)
    # getBookList(links)
    # print(total_briefs_dict)
    # 下载
    # foreachDownload()
    a_connected_sequence()



if __name__ == '__main__':
    # main()
    voluntarily()
    # content=get_contents("https://wap.ibiquges.org/wapbook/8345_3734159.html")
    # print(content)
    # waphtml('https://wap.ibiquges.org/wapbook/118611.html',"青川十四")
    # print(total_briefs_dict)
    # for i in range(1, 101):
    #     print("\r", end="")
    #     print("进度: {}%: ".format(i), "▓" * (i // 2), end="")
    #     sys.stdout.flush()
    #     time.sleep(0.05)