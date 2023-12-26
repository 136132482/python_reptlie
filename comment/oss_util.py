import os.path

import oss2
from itertools import islice

import yaml
from  comment import  base64util

# 1 代码嵌入方式配置

# 填写RAM用户的访问密钥（AccessKey ID和AccessKey Secret）。
with open('crypto_config.yaml', 'r') as file:
    config = yaml.safe_load(file)

# 访问配置选项
accessKeyId = config['oss_ask']['accessKeyId']
accessKeySecret = config['oss_ask']['accessKeySecret']
key = config['oss_ask']['key']
# 使用代码嵌入的RAM用户的访问密钥配置访问凭证。
auth = oss2.Auth(base64util.aes_decode(accessKeyId,key), base64util.aes_decode(accessKeySecret,key))

# endpoint填写Bucket所在地域对应的Endpoint。以华东1（杭州）为例，Endpoint填写为https://oss-cn-hangzhou.aliyuncs.com。
endpoint = 'http://oss-cn-beijing.aliyuncs.com'

# 填写Bucket名称。
bucketName = 'cwl1113-demo'
bucket = oss2.Bucket(auth, endpoint, bucketName)

# 上传文件到OSS。
# objectName由包含文件后缀，不包含Bucket名称组成的Object完整路径，例如abc/efg/123.jpg。
objectName = 'test'
# localFile由本地文件路径加文件名包括后缀组成，例如/users/local/myfile.txt。
localFile = 'E:\\VSCodePros\\PYTHON\\OSS\\test001.txt'

save_path="F:\\test_voice"

def   uoload_oss(localFile):
    global objectName
    name=os.path.basename(localFile)
    objectName=objectName+"/"+name
    result=bucket.put_object_from_file(objectName, localFile)
    print(result)
    # 生成下载链接
    fileLink = 'http://'+bucketName+'.oss-cn-shanghai.aliyuncs.com/'+objectName
    print(fileLink)
    url=bucket.sign_url('GET', objectName,60)
    return url


def  down_oss(objectName,save_path):
    #下载OSS文件到本地文件。
    # objectName由包含文件后缀，不包含Bucket名称组成的Object完整路径，例如abc/efg/123.jpg。
    # localFile由本地文件路径加文件名包括后缀组成，例如/users/local/myfile.txt。
    bucket.get_object_to_file(objectName, save_path)

def  list_oss():
    # oss2.ObjectIterator用于遍历文件。列举10个文件
    for b in islice(oss2.ObjectIterator(bucket), 10):
        print(b.key)

def  list_all_oss():
    # 列举Bucket下的所有文件。
    for obj in oss2.ObjectIterator(bucket):
        print(obj.key)


def  prefix_list():
    # 列举指定前缀的所有文件
    # 列举fun文件夹下的所有文件，包括子目录下的文件。
    for obj in oss2.ObjectIterator(bucket, prefix='fun/'):
        print(obj.key)

def  marker_list():
    # 列举指定起始位置后的所有文件
    # 列举指定字符串之后的所有文件。即使存储空间中存在marker的同名object，返回结果中也不会包含这个object。
    for obj in oss2.ObjectIterator(bucket, marker="x2.txt"):
        print(obj.key)

def  dir_list():
    # 列举指定目录下的文件和子目录
    # 列举fun文件夹下的文件与子文件夹名称，不列举子文件夹下的文件。
    for obj in oss2.ObjectIterator(bucket, prefix = 'fun/', delimiter = '/'):
        # 通过is_prefix方法判断obj是否为文件夹。
        if obj.is_prefix():  # 判断obj为文件夹。
            print('directory: ' + obj.key)
        else:                # 判断obj为文件。
            print('file: ' + obj.key)

# 获取指定目录下的文件大小
def CalculateFolderLength(bucket, folder):
        length = 0
        for obj in oss2.ObjectIterator(bucket, prefix=folder):
            length += obj.size
            return length
        for obj in oss2.ObjectIterator(bucket, delimiter='/'):
            if obj.is_prefix():  # 判断obj为文件夹。
                length = CalculateFolderLength(bucket, obj.key)
                print('directory: ' + obj.key + '  length:' + str(length) + "Byte.")
            else: # 判断obj为文件。
                print('file:' + obj.key + '  length:' + str(obj.size) + "Byte.")


if __name__ == '__main__':
    path="F:\\test_voice"
    url=uoload_oss("F:\\test_voice\\audio.mp3")
    print(url)
    # path=path+"\\"+"test.wav"
    # down_oss("test/audio.wav",path)
     # print(reslut)