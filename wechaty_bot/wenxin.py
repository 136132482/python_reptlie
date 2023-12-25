#文心一言  暂时没有钱
import os
import requests
from PIL import Image
from io import BytesIO

import wenxin_api # 可以通过"pip install wenxin-api"命令安装
from wenxin_api.tasks.text_to_image import TextToImage
wenxin_api.ak='UGByNQEQgWQ9my1Tg8qHEjMS4lw7Nl1c'
wenxin_api.sk='QAd0paeXVKS02P57VZhvCP2MywdliCaH'

pic_path_test="F:\\model_test\\pic_test"


def  text_to_image(input_txt):
    input_dict = {
        "text": input_txt,
        "style": "插画",
        "num": 20
    }
    rst = TextToImage.create(**input_dict)  # 转换成关键字参数传递给接口
    # rst dict类型
    print(rst)

    # 显示图片
    imgUrls = rst["imgUrls"]  # 提取图片地址，list格式
    # if os.path.exists("./imgs/"):shutil.rmtree("./imgs/")    # 删除文件夹
    if not os.path.exists(pic_path_test): os.makedirs(pic_path_test)  # 不存在则新建文件夹
    i = 0
    for imurl in imgUrls:
        # print(imurl)
        # show_img(imurl)
        file_name = os.path.join(pic_path_test + str(i) + ".jpg")
        images_save_and_show(imurl, file_name)
        i += 1





def images_save_and_show(url,name):
    # 图片的URL
    # url = 'http://example.com/image.jpg'
    # 使用requests库从URL获取图片
    response = requests.get(url)
    # 检查请求是否成功
    if response.status_code == 200:
        # 打开图片并展示
        img = Image.open(BytesIO(response.content))
        img.show()
        # 或者保存图片到本地
        img.save(name)
    else:
        print("请求失败，状态码：", response.status_code)

if __name__ == '__main__':
    text_to_image("熊猫人开心表情,最好是比较搞笑的,大自然")