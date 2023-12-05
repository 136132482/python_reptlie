import binascii
import os
import shutil
import difflib

import requests
from Crypto.Cipher import AES
import base64
import binascii

from reptliie_picture import taotu_reptile

# import Levenshtein
save_path1="F:\BeautifulPictures/taotu/"


def get_file_names(directory):
    file_names = os.listdir(directory)
    return file_names
# 调用函数获取文件夹中所有文件的名称
file_names = get_file_names(save_path1)
# 打印文件名称
# for file_name in file_names:
#     path=save_path1 + "/" + file_name
#     files = [os.path.join(path, file) for file in os.listdir(path)]



file_dict={}
file_ls = set()
def  recursion(path,n):
    # files = [os.path.join(path, file) for file in os.listdir(path)]
    files = os.listdir(path)
    # print(files)
    for file in files:
         file_p = os.path.join(path, file)
         if os.path.isdir(file_p):
          recursion(file_p,n+1)
         else:
            # parent_dir, file_name = path.rsplit('/', 1)
            findRootdirName(file,file_p)


def  findRootdirName(fl,file_path):
    if file_path.endswith(".jpg"):
        # print(fl+"--------------------")
        file=fl.rsplit("(", 1)
        if file[0].endswith('.jpg'):
            os.remove(file_path)
        else:
            # print(file)
            # print(file_path)
            path1=os.path.split(file_path)[0]
            path2=os.path.split(path1)[0].rsplit("/",1)[1]
            #如果当前的名字和当前的路径文件夹名字不相等
            if file[0]!=path2:
                source_path=os.path.join(save_path1, file[0])
                directory_list = os.listdir(source_path)
                subdirectories = [d for d in directory_list if os.path.isdir(os.path.join(source_path, d))]
                # for subdir in subdirectories:
                target_dir=os.path.join(source_path, subdirectories[0])
                target_file = os.path.join(target_dir, fl)
                print(target_file)
                if os.path.exists(target_file):
                    os.remove(target_file)
                shutil.move(file_path, target_dir)
                print("开始移动"+file_path+"至"+target_dir+"文件夹成功")


def main():
    # dir_path()
    # for flie in file_child:
        recursion(save_path1, 1)

    # func(save_path1,1)

    # func(save_path1,1)
    # findRootdirName(save_path1)
    # a = '[Minisuka.tv]SeiaFujii藤井星愛-Regular'
    # b = '[Minisuka.tv]SeiaFujii藤井星愛-RegularGallery2.2(48P)0.jpg'
    # distance = Levenshtein.distance(a, b)
    # print(distance)
    # ratio = difflib.SequenceMatcher(None, a, b).ratio()
    # print(ratio)
    # b=b.rsplit("(",1)
    # b=b[0]
    # print(b)


file_child=set()
def  dir_path():
  for root,dirs,files in  os.walk(save_path1):
      # print("当前目录：", root)
      # print("子目录列表：", dirs)
      # print("文件列表：", files)
      if root != save_path1:
          if len(dirs) !=0 and len(dirs) ==1:
              # print(root)
              # print(dirs[0])
              path = os.path.join(root,dirs[0])
              file_child.add(path)


def func(filepath, n):
    files = os.listdir(filepath)
    # 获取到文件的路径
    for file in files:
        file_p = os.path.join(filepath, file)
        if os.path.isdir(file_p):
            print('\t*n', file)
            func(file_p, n + 1)
        else:
            print('\t*n', file_p)

def give_ts():
    filename = 'video-123' + '.ts'
    ts_url="https://tp5.panqing80.club/videos3/25706b7b99d864158c4a607c96dc94eb/25706b7b99d864158c4a607c96dc94eb7.ts?auth_key=1701610031-96-0-c5bb7ca5666309e17efc4c895950cf95"
    res_ts = requests.get(ts_url, headers=taotu_reptile.headers).content
    # 下载的 video-0000.ts video-0213.ts 文件保存目录
    with open('C:\\Users\\ALIENWARE\\Downloads/' + filename, 'wb') as ts:
        # 解密
        cryptor = AES.new("1701610031-96-0-c5bb7ca5666309e17efc4c895950cf95", AES.MODE_CBC, binascii.a2b_hex('25706b7b99d864158c4a607c96dc94eb7'))
        ts.write(cryptor.decrypt(res_ts))
        print('下载:' + filename)
print('下载完成')



if __name__ == '__main__':
    # main()
    give_ts()