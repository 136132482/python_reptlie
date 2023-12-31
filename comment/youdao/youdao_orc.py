# -*- coding: utf-8 -*-
import os
import sys
import uuid
import requests
import base64
import hashlib
import time
import re
from comment import comment_util

YOUDAO_URL = 'https://openapi.youdao.com/ocrapi'
APP_KEY = '089c55fbbfa57e7f'#自己替换喽
APP_SECRET = 'LWzGxGm7yNbR667LdaJFaTNCJl8JZTZj'
#这玩意要钱的，注册的50元优惠很快就莫的了

def truncate(q):
    if q is None:
        return None
    size = len(q)
    return q if size <= 20 else q[0:10] + str(size) + q[size - 10:size]


def encrypt(signStr):
    hash_algorithm = hashlib.sha256()
    hash_algorithm.update(signStr.encode('utf-8'))
    return hash_algorithm.hexdigest()


def do_request(data):
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    return requests.post(YOUDAO_URL, data=data, headers=headers)

save_path = 'F:\\test_voice\\test_pic\\emoji'

def connect(path_img):
    # if not os.path.exists(save_path):
    #     os.mkdir(save_path)
    # path_save=save_path+'/'+name+'.txt'

    f = open(path_img, 'rb')  # 二进制方式打开图文件
    q = base64.b64encode(f.read()).decode('utf-8')  # 读取文件内容，转换为base64编码
    f.close()

    data = {}
    data['detectType'] = '10012' #代表换行
    data['imageType'] = '1'
    data['langType'] = 'auto' #'zh-CHS'#'auto'
    data['img'] = q
    data['docType'] = 'json'
    data['signType'] = 'v3'
    curtime = str(int(time.time()))
    data['curtime'] = curtime
    salt = str(uuid.uuid1())
    signStr = APP_KEY + truncate(q) + salt + curtime + APP_SECRET
    sign = encrypt(signStr)
    data['appKey'] = APP_KEY
    data['salt'] = salt
    data['sign'] = sign
    try:
        response = do_request(data)
        # print(response.content)
        # 出来乱码，解码之后是str格式，我用split保存关键位置的文字
        results=response.content.decode()
        # print(A)
        # with open(path_save, 'w') as file:
        aticle = results.split('"text":"')[1:]
        if len(aticle)!=0:
            texts=[]
            for line in aticle:
                word = line.split('","lang":')[0]
                texts.append(word)
                # file.write(word)
                # file.write('\n')
            text="".join(texts)
            text = comment_util.remove_special_characters(text)
            # text = ''.join(re.findall('\d+', text))
            print(text)
            file=os.path.basename(path_img)
            format = file.split(".")[1]
            text = text + "." + format
            new_path = os.path.join(save_path, text)
            os.rename(path_img, new_path)
            print("重命名成功：" + text)
    except Exception as e:
         print(e)
         os.remove(path_img)


if __name__ == '__main__':
    # import os
    # import glob
    #
    # path_img='pic'
    # extensions=['jpg', 'JPG', 'jpeg', 'JPEG']
    # for extension in extensions:
    #     for path in glob.glob(os.path.join(path_img,'*.'+extension)):
    #         connect(path)
    files=os.listdir(save_path)
    for file in files:
        path=os.path.join(save_path,file)
        connect(path)