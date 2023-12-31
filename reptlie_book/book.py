# 导入requests库
import asyncio
import threading
import redis
import requests
# 导入文件操作库
import codecs
import os
import sys
import importlib
from bs4 import BeautifulSoup
from tqdm import tqdm, trange
from comment.proxy_util import get_soup, click, click_noproxy
from dynamic_database import test1
from dynamic_database import test2
from dynamic_database  import mysql_DBUtils
from reptlie_book import briefs_dict
from mitmproxy import http
importlib.reload(sys)
import httpx
import time
import colorsys
import concurrent.futures
import progressbar
import re
from comment import pyppeteer_demo
from selenium.webdriver.common.by import By
#驱动放在reptlie_book目录下
mysql = mysql_DBUtils.MyPymysqlPool("dbMysql1")



# r = redis.Redis(host='localhost', port=6379, db=0,decode_responses=True)
# res = r.zremrangebyscore('proxies:universal', 1, 10)
# print(res)
# proxies = r.zrangebyscore('proxies:universal', 10, 100)
# # [print(proxies) for proxies in res]
# redis_proxy = {'HTTPS://': "https://" + random.choice(proxies), 'HTTP://': "http://" + random.choice(proxies)}

num=1
num1=1
num2=1

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
    texts_content = []
    brower=click(chapter)
    get_text(brower,texts_content)
    brower.close()
    # 获取div标签id属性content的内容 \xa0 是不间断空白符 &nbsp;
    texts="\n".join(texts_content)
    content = texts.replace('\xa0' * 4, '\n').replace("最新网址：wap.ibiquges.org","")+"\n"
    texts_content.clear()
    return content


def  get_text(brower,texts_content):
        bf = BeautifulSoup(brower.page_source, 'html.parser')
        texts = bf.find('div', attrs={'id': 'nr1'}).get_text()
        texts_content.append(texts)
        link = bf.find("td", attrs={'class': 'next'}).find('a')
        if link.get_text() == '下一页':
            brower.find_element(By.CLASS_NAME, "next").click()
            get_text(brower,texts_content)




async def  new_text_content(page,browser):
    texts_content = []
    await new_get_texts(page, texts_content, browser)
    print("".join(texts_content))
    # 3s 后关闭浏览器
    # await asyncio.sleep(3)
    await browser.close()
    texts = "\n".join(texts_content)
    content = texts.replace('\xa0' * 4, '\n').replace("最新网址：wap.ibiquges.org", "") + "\n"
    return content



async def  new_get_texts(page,texts_content,brower):
        html = await page.content()
        bf = BeautifulSoup(html, 'html.parser')
        # page.querySelector("#nr1")
        texts = bf.find('div', attrs={'id': 'nr1'})
        if texts is not None:
            texts=texts.get_text()
            texts_content.append(texts)
            link = bf.find("td", attrs={'class': 'next'}).find('a')
            if link.get_text() == '下一页':
                await (await page.querySelector(".next")).click()
                # await asyncio.sleep(2)
                await asyncio.sleep(2)
                # brower.find_element(By.CLASS_NAME, "next").click()
                page=(await brower.pages())[-1]
                await new_get_texts(page,texts_content,brower)

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

async def downnloadBook(chapterName,chapter,bookname,pbar):
    page,browser =await pyppeteer_demo.pyppeteer_test(chapter)
    content=await new_text_content(page,browser)
    chapter = save_path + "/" + bookname+ ".txt"
    write_txt(chapter, content, 'utf8')
    print("\n ["+bookname+"]"+"当前下载章节为:"+chapterName+'下载完成')
    pbar.update(1)


async def downnloadBooksubChapter(chapterBeans,pabr):
    for i in trange(len(chapterBeans)):
        chapterNameId = chapterBeans[i].get('id')
        chapterName=chapterBeans[i].get('章节名称')
        chapterName=remove_special_characters(chapterName)
        chapterName=str(chapterNameId)+chapterName
        chapter= chapterBeans[i].get('章节url')
        bookname=chapterBeans[i].get('书名')
        page, browser = await pyppeteer_demo.pyppeteer_test(chapter)
        content = await new_text_content(page, browser)
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
async def foreachDownload():
    with concurrent.futures.ThreadPoolExecutor() as exectuor:
        total_briefs_dict=briefs_dict.total_briefs_dict
        for i in range(0,len(list(total_briefs_dict.keys()))):
            bookname= list(total_briefs_dict.keys())[i]
            values = list(total_briefs_dict.values())[i]
            await thread_submit(values,bookname)
    # exectuor.shutdown(wait=True)


async def  thread_submit(values,bookname):
        section_urls = values['章节url']
        bookname = bookname.strip().split("\n")
        with tqdm(total=len(section_urls)) as pbar:
            for i in range(0, len(section_urls)):
                key = list(section_urls.keys())[i]
                value = list(section_urls.values())[i]
                await downnloadBook(key, value, bookname[0],pbar)
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
def save_datas(tableName,columns,insert_datas,*args):
    test2.beansFieldtoPackage(tableName)
    test2.packageList(tableName,columns,insert_datas,*args)




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
    # total_briefs_dict=briefs_dict.total_briefs_dict
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

def exists_index(tableName,index_name,*args):
    show_sql=f"SHOW INDEX FROM {tableName} WHERE Key_name = '{index_name}' "
    res=mysql.getOne(show_sql)
    print(res)
    if res  is False:
        index_sql=f"ALTER table {tableName} add  UNIQUE index {index_name}("
        files=[]
        for arg in args:
            files.append(arg)
        file=",".join(files)
        index_sql+=file+")"
        mysql.insert(index_sql)



def  choice_downnormysql():
    while True:
        try:
            nums = input("请选择数字 1:下载到本地 2：下载到数据库")
            if nums =='1':
                # 下载
                asyncio.get_event_loop().run_until_complete(foreachDownload())
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
    # voluntarily()
    # content=get_contents("https://wap.ibiquges.org/wapbook/8345_3734159.html")
    # print(content)
    # waphtml('https://wap.ibiquges.org/wapbook/118611.html',"青川十四")
    # print(total_briefs_dict)
    # for i in range(1, 101):
    #     print("\r", end="")
    #     print("进度: {}%: ".format(i), "▓" * (i // 2), end="")
    #     sys.stdout.flush()
    #     time.sleep(0.05)
    # proxies = r.zrange('proxies:universal', 0, -1)
    # res=r.zremrangebyscore('proxies:universal',1,10)
    # print(res)
    # res=r.zrangebyscore('proxies:universal',10,100)
    # [print(proxies) for proxies in res]
    # # proxy = {'HTTPS://': "https://" + random.choice(proxies), 'HTTP://': "http://" + random.choice(proxies)}

     asyncio.get_event_loop().run_until_complete(foreachDownload())