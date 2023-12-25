
import matplotlib.pyplot as plt
import paddlehub as hub    # 导入paddlehub
import os #  文件系统操作对象
import shutil
from comment import comment_util
os.environ['HUB_HOME'] = 'F:\\model_test\\paddlehub'
os.environ['WENXIN_AK']='UGByNQEQgWQ9my1Tg8qHEjMS4lw7Nl1c'
os.environ['WENXIN_SK']='QAd0paeXVKS02P57VZhvCP2MywdliCaH'


# 通过paddlehub调用文心大模型  这个也没钱
model = hub.Module(name='ernie_zeus')    # 导入模型,用于情感分析
ernie_vilg_module = hub.Module(name='ernie_vilg')    # 导入模型，用于画图

txt_comment = "这家店味道不错，下次可以再来"
input_dict = {
    "text": f"\"{txt_comment}\",这句话是正面的还是负面的?",
    "task_prompt": "SentimentClassification"
}
result = model.custom_generation(**input_dict)    # 获取情感分析
print(result)

txt_mood = "伤心难过"    # 心情描述
# if "正" in result:
#     txt_mood = "开心高兴"

fd_imgs = "F:\\test_pic"
# 图片保存目录
if os.path.exists(fd_imgs):shutil.rmtree(fd_imgs)    # 删除文件夹

input_dict = {
    "text_prompts" : f"Q版表情,一只{txt_mood}的橙子",    # 提示词
    "style" : "油画",    # 图片类型，水彩，油画，粉笔画，卡通，蜡笔画，儿童画
    "topk" : 1,    # 图片数量，最大10
    "output_dir" : fd_imgs    # 图片保存目录
}
results = ernie_vilg_module.generate_image(**input_dict)    # 生成图片

# 返回的results 就是图片列表,PIL的Image格式
# 显示图片
# 定义一个用于显示图片的函数
def show_pic(pic):
    plt.figure(dpi = 144)
    plt.axis('off')
    plt.imshow(pic)
for pic in results:
    show_pic(pic)