# 创建文件夹
import asyncio
import os
import threading

import pandas as pd
from pydub import AudioSegment
import subprocess
import ffmpeg
import pysilk
import re

def createFile(file_path):
    if os.path.exists(file_path) is False:
        os.makedirs(file_path)
    # 切换路径至上面创建的文件夹
    os.chdir(file_path)



def silk_to_pcm(silk_file, pcm_file):
    command = [
        "ffmpeg",
        "-i", silk_file,
        "-f", "s16le",
        "-acodec", "pcm_s16le",
        pcm_file
    ]
    subprocess.run(command)


from pydub import AudioSegment


def convert_slk_to_wav(slk_file_path, wav_file_path):
    # 读取SLK文件
    with open(slk_file_path, 'rb') as file:
        slk_data = file.read()

    # 将SLK数据转换为音频段
    audio_segment = AudioSegment(
        data=slk_data,
        frame_rate=16000,  # 假设SLK文件的采样率为16000Hz，根据实际情况进行调整
        sample_width=2,  # 假设SLK文件的采样宽度为16位（2字节），根据实际情况进行调整
        frame_count=len(slk_data) // 2  # 计算帧数，假设采样宽度为2字节
    )

    # 将音频段保存为WAV文件
    audio_segment.export(wav_file_path, format="wav")

def   ffmpeg_aur( input_file,output_file):
     input=ffmpeg.input(input_file)
     output=ffmpeg.output(input,output_file)
     ffmpeg.run(output)


slik_path="F:\\BaiduNetdiskDownload\\silk_v3_decoder.exe"
def  silk_change(input_path,pcm_path):
      command = [
            slik_path,
            input_path,
            pcm_path
       ]
      subprocess.run(command)
      subprocess.run("taskkill -f -t -im silk_v3_decoder.exe")

ffmpeg_path="E:\\ffmpeg\\ffmpeg-2023-12-18-git-be8a4f80b9-full_build\\bin\\ffmpeg.exe"
def  ffmpeg_change(pcmPath,target):
    command = [
          ffmpeg_path,
              "-y",
              "-f",
              "s16le",
              "-ar",
              "24000",
              "-ac",
              "1",
              "-i",
              pcmPath,
              target
      ]
    subprocess.run(command)

def  voice_to_wav(path,pcmPath,target):
    silk_change(path,pcmPath)
    ffmpeg_change(pcmPath,target)




count=20
#字典多线程
def split_dict_by_count(datas, count):
    sub_chapters = []
    keys = list(datas.keys())
    total_keys = len(keys)

    for i in range(0, total_keys, count):
        sub_chapter = {k: datas[k] for k in keys[i:i + count]}
        sub_chapters.append(sub_chapter)
    return sub_chapters


#线程量最好根据下载单个速率进行分段 如果速率过快的线程就没必要 设定分段数量过小
#object 实例化对象 methodName 对象方法名 *args 参数
def threadDownnload(datas,object,methodName,*args):
    if isinstance(datas,list):
        sub_lists = [datas[i:i + count] for i in range(0, len(datas), count)]
    if isinstance(datas,dict):
        sub_lists = split_dict_by_count(datas, count)
    # pbar = tqdm(total=len(sub_lists)) #进度条 总计
    threads = []
    for sub_list in sub_lists:
        # print(sub_list) 需要进度条就自己家一个
        t = threading.Thread(target=__thread_download_by_getattr, args=(sub_list,object,methodName,*args))
        threads.append(t)
        t.start()

    # 等待所有线程执行完毕
    for t in threads:
        t.join()



async def threadDownnload_async(datas,object,methodName,*args):
    if isinstance(datas,list):
        sub_lists = [datas[i:i + count] for i in range(0, len(datas), count)]
    if isinstance(datas,dict):
        sub_lists = split_dict_by_count(datas, count)
    # pbar = tqdm(total=len(sub_lists)) #进度条 总计
    tasks = []
    for sub_list in sub_lists:
        # print(sub_list) 需要进度条就自己家一个
        task= asyncio.create_task(__thread_download_by_getattr(sub_list,object,methodName,*args))
        tasks.append(task)
    # 等待所有线程执行完毕
    await  asyncio.gather(*tasks)







async def threadDownnloadNoarg_async(datas,object,methodName):
   await __thread_download_by_getattr_async(datas, object, methodName, None)

async def __thread_download_by_getattr_async(sub_list, object, methodName,*args):
    method = getattr(object, methodName)
    if args[0] is None:
        return  await method(sub_list)
    else:
        return await method(sub_list, *args)




def threadDownnloadNoarg(datas,object,methodName):
   __thread_download_by_getattr(datas, object, methodName, None)
# #进度条自己添加
# def __thread_download_by_getattr(sub_list,object,methodName,pbar,*args):
#       method= getattr(object,methodName)
#       if args is None:
#           return method(sub_list,pbar)
#       else:
#          return method(sub_list,pbar,*args)

def __thread_download_by_getattr(sub_list, object, methodName,*args):
    method = getattr(object, methodName)
    if args[0] is None:
        return method(sub_list)
    else:
        return method(sub_list, *args)


def remove_special_characters(string):
    string=string.strip()
    string = string.replace(">", "")
    string = string.replace("。。", "")
    string = string.replace("`", "")
    string = string.replace(",", "")
    string = string.replace("\\", "")
    string=string.replace(" ","")
    string = string.replace("/", "")
    string = string.replace("?", "")
    string = string.replace("\"", "")
    string = string.replace("\n", "")
    string = string.replace("！", "")
    string = string.replace("！", "")
    string = string.translate(str.maketrans('', '', '@#$%^&*()_+'))
    return string


def has_chinese(string):
    pattern = re.compile("[\u4e00-\u9fa5]")  # Unicode范围内的汉字编码
    result = re.search(pattern, string)
    if result is not None:
        return True
    else:
        return False

if __name__ == '__main__':
    path="F:\\test_voice\\message-4670396532500881838-audio.slk"
    pcmPath =  "F:\\test_voice\\audio.pcm"
    target = "F:\\test_voice\\audio.mp3"
    # createFile(out_path)
    # 使用函数
    # silk_to_pcm()
    # pysilk.encode_file(open(path, "rb"), out_path)
    # 调用函数进行转换
    # convert_slk _to_wav(path, out_path)
    # ffmpeg_aur(path,out_path)
    silk_change(path,pcmPath)
    # pcmPath = "F:\\test_voice\\audio.pcm"
    ffmpeg_change(pcmPath,target)
