import os
from http import HTTPStatus
from urllib.parse import urlparse, unquote
from pathlib import PurePosixPath
import stat
import dashscope
import requests
from dashscope import ImageSynthesis

from comment import comment_util
from comment.youdao import youdao

dashscope.api_key="sk-2262f4bc3f1946038c0e8c62f197e577"

model = "stable-diffusion-v1.5"
# prompt = "帮我生成个熊猫人开心表情包"


def sample_block_call(prompt):
    prompt = youdao.translator(prompt, "en")
    rsp = ImageSynthesis.call(model=model,
                              prompt=prompt,
                              negative_prompt="garfield",
                              n=1,
                              size='1024*1024')
    if rsp.status_code == HTTPStatus.OK:
        print(rsp.output)
        print(rsp.usage)
        # save file to current directory
        for result in rsp.output.results:
            file_name = PurePosixPath(unquote(urlparse(result.url).path)).parts[-1]
            with open('./%s' % file_name, 'wb+') as f:
                f.write(requests.get(result.url).content)
    else:
        print('Failed, status_code: %s, code: %s, message: %s' %
              (rsp.status_code, rsp.code, rsp.message))


async def sample_async_call(prompt,imagename):
    prompt = youdao.translator(prompt, "en")
    rsp = ImageSynthesis.async_call(model="stable-diffusion-xl",
                                    prompt=prompt,
                                    steps=10,
                                    scale=5,
                                    # negative_prompt="garfield",
                                    n=1,
                                    size='512*512')
    if rsp.status_code == HTTPStatus.OK:
        print(rsp.output)
        print(rsp.usage)
    else:
        print('Failed, status_code: %s, code: %s, message: %s' %
              (rsp.status_code, rsp.code, rsp.message))
    status = ImageSynthesis.fetch(rsp)
    if status.status_code == HTTPStatus.OK:
        print(status.output.task_status)
    else:
        print('Failed, status_code: %s, code: %s, message: %s' %
              (status.status_code, status.code, status.message))

    rsp = ImageSynthesis.wait(rsp)
    if rsp.status_code == HTTPStatus.OK:
        print(rsp.output)
        msg= rsp.output.results[0].url
        img_path = 'F:\\test_voice\\test_pic'
        comment_util.createFile(img_path)
        os.chmod(img_path, stat.S_IRWXU)
        img_path=os.path.join(img_path,imagename)
        with open(img_path, 'wb+') as f:
            f.write(requests.get(msg).content)
    else:
        print('Failed, status_code: %s, code: %s, message: %s' %
              (rsp.status_code, rsp.code, rsp.message))


if __name__ == '__main__':
    # sample_block_call("过年照片")
    sample_async_call("这张图片是一个动态的卡通表情包。图中是一只全身雪白，有着黑眼圈和耳朵的熊猫形象，它看起来像是在哭泣或者受了委屈，嘴巴微微张开，眼中含泪，给人一种楚楚可怜的感觉。它的脖子上系着一个红色蝴蝶结，脚下还有一个小小的“JX”标志。整体来说，这个熊猫的形象非常可爱且富有表现力")