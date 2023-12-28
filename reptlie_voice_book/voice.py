import base64
import concurrent
import operator
import threading
import time
from concurrent.futures import ThreadPoolExecutor

# from translate  import Translator
# from tempfile import TemporaryFile
# import speech_recognition as sr #语音识别模块
from  playsound import playsound
# from   gtts  import  gTTS
import os
# import pyttsx3
from progressbar import progressbar
# from pygame import mixer
from dynamic_database  import mysql_DBUtils
from reptliie_picture import taotu_reptile
from reptlie_voice_book import youdao
from reptlie_book import  book
mysql = mysql_DBUtils.MyPymysqlPool("dbMysql1")
from itertools import groupby
import concurrent.futures
from tqdm.asyncio import tqdm, tqdm_asyncio, trange
import edge_tts
import asyncio
import unicodedata
from comment import comment_util
import codecs
book_res=[]
def  choice_downn():
    global book_res
    sql = "select * from reptlie_book "
    keywords=''
    while True:
        try:
            nums = input("请选择 1：查看数据库所有数据 2：搜索（作者或者书名）\n")
            if nums =='1':
                res = mysql.getAll(sql)
                if res is False:
                    print("数据库暂无图书，请使用一键下载功能，快去下载吧~~~")
                    os._exit()
                book_res = res
                break
            elif nums=='2':
                keywords = input("请输入搜索文字（作者或者书名）")
                sql += f"where  书名 like  concat('%','{keywords}','%') or 作者 like concat('%','{keywords}','%') "
                res = mysql.getAll(sql)
                if res is False:
                   num=input("未查到对应数据，请确认  1:重新搜索 2:退出")
                   if num =='1':
                       choice_downn()
                       break
                   elif   num =='2':
                       os._exit()
                   else:
                       print("你输入的命令无效")
                       os._exit()
                book_res = res
                break
            else:
                raise
        except Exception as e :
            print(e)
            print("你输入的不正确，请重新输入")



def  choice_again_downn():
    while True:
        try:
            keywords = input("请输入搜索文字（作者或者书名）")
            if keywords !='' or keywords is not None:
                break
            else:
                raise
        except Exception as e :
            print(e)
            print("你输入的不正确，请重新输入")
    return keywords

def  searchbooklist(keywords):
    sql = "select * from reptlie_book "
    if keywords is not None or keywords != '':
        sql += f"where  书名 like  concat('%',{keywords},'%') or 作者 like concat('%',{keywords},'%') "
    res = mysql.getAll(sql)


book_links = []
#第一步 把数据库的数据展示出来
def  getBookList():
    global book_links
    book_links.clear()
    count=0
    for re  in  book_res:
         field_list=[]
         for key,value in re.items():
             if key =='id':
                book_links.append(value)
             if key =='简介':
                 value = value.replace("\n","").strip()
             field=str(key)+":"+str(value)
             field_list.append(field)
         count+=1
         book_str="\n".join(field_list)
         book_str=f"({count})\n" +book_str+"\n"
         print("")
         print(book_str)


thread_count=20

#这个是用list 干
def threadDownnload(chapter_datas):
    pbar=tqdm(total=len(chapter_datas))
    sub_lists = [chapter_datas[i:i + thread_count] for i in range(0, len(chapter_datas), thread_count)]
    print(sub_lists)
    threads = []
    for sub_list in sub_lists:
        t = threading.Thread(target=book.downnloadBooksubChapter, args=(sub_list,pbar))
        threads.append(t)
        t.start()

    # 等待所有线程执行完毕
    for t in threads:
        t.join()


async def new_threadDownnload(chapter_datas):
    pbar=tqdm(total=len(chapter_datas))
    sub_lists = [chapter_datas[i:i + thread_count] for i in range(0, len(chapter_datas), thread_count)]
    print(sub_lists)
    tasks = []
    for sub_list in sub_lists:
        task = asyncio.create_task(book.downnloadBooksubChapter(sub_list,pbar))
        tasks.append(task)

    await asyncio.wait(*tasks)


#先要把这个对应bookurl数据查出来
def getBookChapterurl():
    if len(sub_book_links)==1:
        sub_book_links.append(sub_book_links[0])
    tupleids=tuple(sub_book_links)
    sql = f"select rbu.*,rb.书名 from reptlie_book_url rbu left join reptlie_book rb on rbu.reptlie_book_id=rb.id where reptlie_book_id in {tupleids} "
    res = mysql.getAll(sql)
    if res is False:
        raise ValueError("未检索到该数数据,请检查该书是否下载到数据库")
    # print(res)
    # user_sort=sorted(res,key=lambda x:x['章节名称'])
    group_res=groupby(res,key=lambda x:x['书名'])
    group_tict={}
    for key,group in group_res:
        group_tict[key]=list(group)
    return group_tict


async def  downbookList(res):
    size=len(list(res.keys()))
    with concurrent.futures.ThreadPoolExecutor() as exectuor:
         tasks=[]
         for i  in range(0,size):
             name=list(res.keys())[i]
             values=res[name]
             # loop = asyncio.get_event_loop()
             task= asyncio.create_task(excutortBook(name,values))
             tasks.append(task)
             # sync(excutortBook(name, values))
    # exectuor.shutdown(wait=True)
    await asyncio.gather(*tasks)


async def  excutortBook(name,values):
    path = os.path.join(book.save_path, name)
    print(path)
    taotu_reptile.createFile(path)
    await new_threadDownnload(values)



#去除已经下载的书籍
def estimateBook(group_tict):
    exists_group_tict={}
    books=list(group_tict.keys())
    for i in range(0,len(books)):
       if os.path.exists(os.path.join(book.save_path,books[i])):
           continue
       else:
           value=group_tict[books[i]]
           exists_group_tict[books[i]]=value
    return exists_group_tict

def estimateBookmp3(group_tict):
    exists_group_tict=[]
    books=list(group_tict.keys())
    for i in range(0,len(books)):
       if os.path.exists(os.path.join(save_mp3_path,books[i])):
           continue
       else:
           value = group_tict[books[i]]
           exists_group_tict[books[i]] = value
    return exists_group_tict

def saveDownBook():
    choice_downn()
    getBookList()
    get_true()
    group_tict=getBookChapterurl()
    print(group_tict)
    # exists_group_tict=estimateBook(group_tict)
    # #下载文本
    # if len(exists_group_tict)==0:
    #    print("你要下载的书籍已存在")
    #    os.exit()
    # downbookList(group_tict)
    asyncio.get_event_loop().run_until_complete(downbookList(group_tict))
    # exists_group_tict_mp3 = estimateBookmp3(group_tict)
    # if len(exists_group_tict_mp3) == 0:
    #     print("你要下载的书籍mp3已存在")
    #     os.exit()



# 使用asyncio创建一个异步协程
# async def async_operation():
#     print("开始异步操作")
#     sub_list_book= convert_text()
#     loop = asyncio.get_running_loop()
#     # 在线程池中运行阻塞IO操作
#     await loop.run_in_executor(executor, thread_mp3_downnload, sub_list_book)
#     # print(result)

def  book_change_mp3():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(convert_text())


sub_book_links=[]
def  get_true():
    global sub_book_links
    while True:
        try:
            nums = input("请输入你想下载的书籍id,是id不是序号！！！(可多选,以逗号隔开,不选取数字直接enter确认默认下载所有,重新选择输入#号建)\n")
            if nums is None or nums =='':
              sub_book_links=book_links
              break
            elif nums =='#':
               saveDownBook()
               break
            else:
              list_nums = nums.split(",")
              my_list = [int(i) for i in list_nums]
              if all( x in book_links for x in my_list):
                  sub_book_links = my_list
              else:
                  print("你输入的id中有不在数据列表中的元素，请重新输入 ")
                  get_true()
              break
        except Exception as e :
            print(e)
            print("你输入的不正确，请重新输入")
    return  sub_book_links



sub_list_book=[]
def  get_connvert(list_book):
    global sub_list_book
    while True:
        try:
            nums = input("请选择你要文本对应转换的书名序号(可多选，以逗号隔开，不选取数字直接enter确认默认下载所有,重新选择输入#号建\n")
            if nums is None or nums =='':
              sub_list_book=list(list_book.values())
              break
            elif nums =='#':
               get_connvert(list_book)
               break
            else:
              list_nums = nums.split(",")
              my_list = [int(i) for i in list_nums]
              list_book_num=list(list_book.keys())
              if all( x in list_book_num for x in my_list):
                  sub_list_book = [list_book[i] for i in my_list]
              else:
                  print("你输入的序号中有不在数据列表中的元素，请重新输入 ")
                  get_connvert(list_book)
              break
        except Exception as e :
            print(e)
            print("你输入的不正确，请重新输入")
    return  sub_list_book

async def convert_text():
    #获取到下载对应的文件名称
    files=os.listdir(book.save_path)
    list_book=[]
    for file in files:
       if os.path.isdir( os.path.join(book.save_path,file)):
           list_book.append(file)
    books_mp3={}
    print("\n此为刚下载的书架，请选择\n")
    for  i  in range(len(list_book)):
      print("("+str(i)+")"+list_book[i]+"\n")
      books_mp3[i]=list_book[i]
    sub_list_book=get_connvert(books_mp3)
    print(sub_list_book)
    await thread_mp3_downnload(sub_list_book)
# executor = ThreadPoolExecutor()
async def  thread_mp3_downnload(sub_list_book):
    # with concurrent.futures.ThreadPoolExecutor() as exectuor:
    #    await exectuor.map(get_book_files,sub_list_book)
        for i in range(len(sub_list_book)):
             await get_book_files(sub_list_book[i])
             # loop = asyncio.get_running_loop()
             # # 在线程池中运行阻塞IO操作
             # await loop.run_in_executor(exectuor, get_book_files, sub_list_book[i])
             # loop.close()
           # await exectuor.submit(get_book_files, sub_list_book[i])
    # exectuor.shutdown(wait=True)


async def  get_book_files(bookname):
    path = os.path.join(book.save_path, bookname)
    files = os.listdir(path)
    files = sorted(files)
    print("当前下载的小说名称为："+bookname+",共计章节："+str(len(files))+"章")
    [print(file) for file in files]
    mp3_filepath=os.path.join(save_mp3_path, bookname)
    taotu_reptile.createFile(mp3_filepath)
    await choice_voice(files,bookname)






# def pyttsx3_debug(text,language,rate,volume,filename,sayit=0):
#     #参数说明: 六个重要参数,阅读的文字,语言(0-英文/1-中文),语速,音量(0-1),保存的文件名(以.mp3收尾),是否发言(0否1是)
#     engine = pyttsx3.init()  # 初始化语音引擎
#     engine.setProperty('rate', rate)  # 设置语速
#     #速度调试结果:50戏剧化的慢,200正常,350用心听小说,500敷衍了事
#     engine.setProperty('volume', volume)  # 设置音量
#     voices = engine.getProperty('voices')  # 获取当前语音的详细信息
#     if int(language)==0:
#         engine.setProperty('voice', voices[0].id)  # 设置第一个语音合成器 #改变索引，改变声音。0中文,1英文(只有这两个选择)
#     elif int(language)==1:
#         engine.setProperty('voice', voices[1].id)
#     if int(sayit)==1:
#         engine.say(text)  # pyttsx3-&gt;将结果念出来
#     elif int(sayit)==0:
#         print("那我就不念了哈")
#     engine.save_to_file(text, filename) # 保存音频文件
#     print(filename,"保存成功")
#     engine.runAndWait() # pyttsx3结束语句(必须加)
#     engine.stop() # pyttsx3结束语句(必须加)

# #函数功能: 用gtts库阅读文本,保存为.mp3文件后, 用系统内置的浏览器阅读出来, 打开mp3文件, 函数执行结束(播放方式为os库)
# def gtts_os_debug(text,mp3_filepath,language):#参数说明:参数1是朗读的文字,参数2是保存路径,参数3是数字{0英文,1中文,2日语}
#     #大成功,可惜的是os调用自带播放器, 实际上只执行了"打开mp3"的操作, 它并不会在音频播报完后再进行下一条语句
#     # 已知zh-tw版本违和感较高,所以我们用zh-CN来进行后续工作
#     if int(language) ==0 :
#         s = gTTS(text=text, lang='en', tld='com')
#         # s = gTTS(text=text, lang='en', tld='co.uk')#我比较喜欢美音,但是如果你喜欢英国口音可以尝试这个
#     elif int(language) ==1 :
#         s = gTTS(text=text, lang='zh-CN')
#     elif int(language) ==2 :
#         s = gTTS(text=text, lang='ja')
#     try:
#         s.save(mp3_filepath)
#     except:
#         os.remove(mp3_filepath)
#         print(mp3_filepath,"文件已经存在,但是没有关系!已经删掉了")
#         s.save(mp3_filepath)
#     print(mp3_filepath,"保存成功")
#     os.system(mp3_filepath)#调用系统自带的播放器播放MP3
# # gtts_os_debug(text="I'm gtts library,from google Artificial Intelligence &amp; Google Translate.",mp3_filepath="gtts英文测试.mp3",language=0)
# # gtts_os_debug(text="我是gtts库, 你想听听我的声音吗",mp3_filepath="gtts中文测试.mp3",language=1)
# # gtts_os_debug(text="真実はいつもひとつ" ,mp3_filepath="gtts日语测试.mp3",language=2)

concurrent_downloads=3
semaphore=asyncio.Semaphore(concurrent_downloads)
save_mp3_path='F:\VoiceBook'
#voice 语言  rate 语速 volume 音量
async def  download_files(files,voice,rate,volume,bookname):
    task_list=[]
    file_paths = [os.path.join(book.save_path,bookname, file) for file in files]
    # datas=tqdm(range(len(file_paths)))
    # with datas as pbar:
    for i in range(len(file_paths)):
                # pbar.set_description("当前转化书名:《"+bookname+"》转化章节名称:【"+files[i]+"】")
            task=asyncio.create_task(voice_convert(file_paths[i], voice, rate, volume,bookname))
            task_list.append(task)
                # pbar.update()
    return task_list


async def  async_thread_task(files,voice,rate,volume,book):
    task_list= await download_files(files,voice,rate,volume,book)
    done=await tqdm_asyncio.gather(*task_list,timeout=None)
    for done_task in done:
         print(str(done_task)+"执行完毕\n\n")


async def  voice_convert(file_path,voice,rate,volume,bookname):
     async with semaphore:
        with open(file_path,"rb") as file:
            txt=file.read()
            txt=txt.decode('utf-8')
            bookpath=os.path.join(save_mp3_path, bookname)
            path = os.path.basename(file_path)  .split(".")[0]
            output=os.path.join(save_mp3_path,bookname,path+".mp3")
            if os.path.exists(bookpath):
                taotu_reptile.createFile(bookpath)
            await my_function(txt,voice,rate,volume,output)
        return  output
async def my_function(TEXT,voice,rate,volume,output):
    tts = edge_tts.Communicate(text=TEXT, voice=voice, rate=rate, volume=volume)
    await tts.save(output)
    return tts


flag_voice=True
flag_rate=True
flag_volume=True
voice=''
rate=''
volume=''
#d
async def  choice_voice(files,booknname):
    datas = await edge_tts.list_voices()
    count=0
    voice_data={}
    for data in datas:
      name= data['Name']
      Local=data['Locale']
      youdao_list=list(youdao.datas.values())
      local=Local[0:2]
      if local in youdao_list:
          voice_data[str(count)] = data
          print("(" + str(count) + ")" + name)
          count += 1
      # translator = Translator(to_lang='zh')
      # translation = translator.translate(name)
    await get_choice_voice(voice_data)
    await choice_rate(voice)
    await choicce_volume(voice,rate)
    await asyncio.sleep(1)
    await async_thread_task(files,voice,rate,volume,booknname)





async def  get_choice_voice(datas):
    global flag_voice
    global voice
    while flag_voice:
        try:
             path = os.path.join(save_mp3_path, "测试音频")
             num = input("请选择对应声音的序号来试听音色,直接enter默认选择云夏音色\n")
             if num==None or num=='':
                 voice="Microsoft Server Speech Text to Speech Voice (zh-CN, YunxiaNeural)"
                 Local="zh-CN"
             else:
                 voice = datas[num]['Name']
                 Local = datas[num]['Locale']
                 print(voice)
                 print(Local)
             field_path=os.path.join(path,voice.replace(" ","")+".mp3")
             print(field_path)
             if  os.path.exists(field_path):
                 playsound(field_path)
             else:
                 if os.path.exists(path):
                     taotu_reptile.createFile(path)
                 text="你好，欢迎来到我的世界,很高兴认识你"
                 text=youdao.translator(text,Local)
                 print(text)
                 tts = edge_tts.Communicate(text=text, voice=voice,rate='+0%',volume='+0%')
                 await tts.save(field_path)
                 await asyncio.sleep(2)
                 playsound(field_path)
             choice=input("请选择是否确认选择该音色，y/s,(y确认，s重新进行选择音色,【试音需要下载,可能会出现指定的设备未打开，或不被 MCI 所识别，继续选择即可】)\n")
             if choice.lower() =='y':
                 flag_voice = False
                 break
             else:
               await  get_choice_voice(datas)
        except Exception as e :
            print("你输入的不正确，请重新输入"+e)
    return  voice

async def  choice_rate(voice):
    global flag_rate
    global rate
    while flag_rate:
        try:
            path = os.path.join(save_mp3_path, "测试音频")
            print(path)
            rate = int(input("请输入语速-100-100中的数字，正常语速为0\n"))
            if rate>100:
                raise
            if rate<-100:
                raise
            if rate>=0:
                rate = f'+{rate}%'
            else:
                rate = f'{rate}%'
            field_path = os.path.join(path, voice + rate + ".mp3")
            if os.path.exists(field_path):
                playsound(field_path)
            else:
                taotu_reptile.createFile(path)
                tts =  edge_tts.Communicate(text="你好，欢迎来到我的世界,很高兴认识你,现在语速为:"+rate, voice=voice, rate=rate)
                await tts.save(field_path)
                await asyncio.sleep(2)
                playsound(field_path)
            choice = input("请选择是否确认选择该语速，y/s,(y确认，s重新进行选择语速,【试音需要下载,可能会出现指定的设备未打开，或不被 MCI 所识别，继续选择即可】)\n")
            print("选择之后的音色，语速，音量在多选下载的情况，直接默认第一次的选定操作进行下载\n")
            if choice.lower() == 'y':
                flag_rate=False
                break
            else:
               await choice_rate(voice)
        except Exception as e:
            print(e)
            print("你输入的不正确，请重新输入")
    return  rate

async def  choicce_volume(voice,rate):
    global flag_volume
    global volume
    while flag_volume:
        try:
            path = os.path.join(save_mp3_path, "测试音频")
            volume = int(input("请输入音量-100-100中的数字，标准音量为0\n"))
            if volume > 100:
                raise
            if volume < -100:
                raise
            if volume >= 0:
                volume = f'+{volume}%'
            else:
                volume = f'{volume}%'
            field_path = os.path.join(path, voice + "语速"+rate +"音量"+volume+ ".mp3")
            if os.path.exists(field_path):
                await asyncio.sleep(1)
                playsound(field_path)
            else:
                taotu_reptile.createFile(path)
                tts = edge_tts.Communicate(text="你好，欢迎来到我的世界,很高兴认识你,现在语速为" + rate+"音量为"+volume, voice=voice,
                                           rate=rate,
                                           volume=volume)
                await tts.save(field_path)
                await asyncio.sleep(2)
                playsound(field_path)
            choice = input("请选择是否确认选择该音量，y/s,(y确认，s重新进行选择音量,【试音需要下载,可能会出现指定的设备未打开，或不被 MCI 所识别，继续选择即可】)\n")
            if choice.lower() == 'y':
                flag_volume=False
                break
            else:
               await choicce_volume(voice,rate)
        except Exception as e:
            print(e)
            print("你输入的不正确，请重新输入")
    return  volume




#主要是用于章节合到一起
def   book_to_change():
    files = os.listdir(book.save_path)
    for file in files:
        file_path=os.path.join(book.save_path, file)
        if os.path.isdir(file_path):
            files_by_book=os.listdir(file_path)
            files.sort()
            name=os.path.basename(file_path)
            file_all_path = os.path.join(file_path, name + ".txt")
            for file in files_by_book:
                path=os.path.join(file_path,file)
                with codecs.open(path,'rb') as f:
                   content=f.read()
                   # 将解码后的bytes转换为字符串
                   # content= unicodedata.normalize('NFKC', content)
                with codecs.open(file_all_path,'ab+') as f:
                    f.write(content)


if __name__ == '__main__':
    # getBookList()

    # gtts_os_debug(text="我是gtts库, 你想听听我的声音吗",mp3_filepath="gtts中文测试.mp3",language=1)
    # mzitu_window.createFile("F:\VoiceBook\帝们的那些事儿")
    # # gtts_os_debug("F:\Book\上帝们的那些事儿/291序那些上帝.txt","F:\Book",1)
    # voice = 'zh-CN-YunxiNeural'
    # output = 'F:\VoiceBook\帝们的那些事儿/292章一第零团队高天峰线.mp3'
    # rate = '-4%'
    # volume = '+0%'
    # book_change_mp3()

    # rate = int(input("请选择语速-100-100中的数字，默认为正常语速0,不选直接enter默认为0\n"))
    #
    # if rate>0:
    #     print("shi"+str(rate))
    # else:
    #     print("bushi"+str(rate))
    # sub_list_book=convert_text()
    # for i in range(len(sub_list_book)):
    #     loop = asyncio.get_event_loop()
    #     loop.run_until_complete(get_book_files(sub_list_book[i]))
    # asyncio.run(convert_text())


    #下载数据库目录
    # saveDownBook()
    # book_change_mp3()
    book_to_change()