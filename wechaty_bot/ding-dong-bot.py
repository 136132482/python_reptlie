"""doc"""
import asyncio
import logging
import stat
from typing import Optional, Union,Dict

from wechaty_grpc.wechaty.puppet import MessageType
from wechaty_puppet import FileBox
from wechaty import Wechaty, Contact
from wechaty.user import Message, Room
from wechaty import Wechaty, MiniProgram
from comment   import  librosa_voice,comment_util
from wechaty_bot import dashscope_demo, paraformer_demo
from wechaty_puppet import ContactType
from wechaty_plugin_contrib.matchers import ContactMatcher

import pysilk
import pandas as pd


import os
os.environ['WECHATY_PUPPET_SERVICE_TOKEN']='puppet_padlocal_8016548d2b554ebbb4f5c89767a83b00'
os.environ['WECHATY_PUPPET']='wechaty-puppet-padlocal'
os.environ['WECHATY_PUPPET_SERVICE_ENDPOINT']='192.168.0.107:7890'

from wechaty_plugin_contrib.contrib import (
    RoomInviterOptions,
    RoomInviterPlugin
)
from wechaty_plugin_contrib.matchers import (
    MessageMatcher,
    RoomMatcher
)

from wechaty_plugin_contrib import (
    AutoReplyRule,
    AutoReplyPlugin,
    AutoReplyOptions,
)

rules: Dict[MessageMatcher, RoomMatcher] = {
    MessageMatcher('进群'): RoomMatcher('44群'),
    MessageMatcher('入群'): RoomMatcher('44群'),
}
plugin = RoomInviterPlugin(options=RoomInviterOptions(
    name='福利群',
    rules=rules,
    welcome='欢迎入群 ～'
))

img_url = 'https://ss0.bdstatic.com/70cFuHSh_Q1YnxGkpoWK1HF6hhy' \
          '/it/u=1257042014,3164688936&fm=26&gp=0.jpg'
dict = {"李白": "刺客", "大招": "千里不流行，十步杀一人"}
plugin_msg = AutoReplyPlugin(options=AutoReplyOptions(
    rules=[
        AutoReplyRule(keyword='ding', reply_content='dong'),
        AutoReplyRule(keyword='七龙珠', reply_content='哇，你好牛逼啊，还看七龙珠'),
        AutoReplyRule(
            keyword='七龙珠',
            reply_content=FileBox.from_url(img_url, name='python.png')
        ),
        # AutoReplyRule(
        #     keyword='网易-李白',
        #     reply_content=MiniProgram.create_from_json({...})
        # )
    ],
    matchers=[
        ContactMatcher(Optional[Wechaty]),
    ]
))





logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(filename)s <%(funcName)s> %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)

log = logging.getLogger(__name__)

img_path='F:\\test_pic'
mp3_path='F:\\test_voice'

host_name="https://3g79q59242.imdo.co/"

async def message(msg: Message) -> None:
    """back on message"""
    from_contact = msg.talker()
    text = msg.text()
    room = msg.room()
# if text == 'ding':
    conversation: Union[
        Room, Contact] = from_contact if room is None else room
    #联系人类型
    if conversation.type() == ContactType.CONTACT_TYPE_PERSONAL:
        if conversation.is_offical():
            return
        if conversation.is_self():
           return
        if conversation.name=='微信团队':
            return
        await conversation.ready()
        # await conversation.say('dong')
        # file_box = FileBox.from_url(
        #     'https://ss3.bdstatic.com/70cFv8Sh_Q1YnxGkpoWK1HF6hhy/it/'
        #     'u=1116676390,2305043183&fm=26&gp=0.jpg',
        #     name='ding-dong.jpg')
        # text=await choice_type(type,msg)
        if msg._payload.type == MessageType.MESSAGE_TYPE_IMAGE:
            file_box_2 = await msg.to_file_box()
            # 将Message转换为FileBox
            os.chmod(img_path, stat.S_IRWXU)
            comment_util.createFile(img_path)
            await file_box_2.to_file(file_path=img_path, overwrite=True)  # 将图片保存为本地文件
            # img_new_path = img_transform(img_in_path)  # 调用图片风格转换的函数
            # file_box_3 = FileBox.from_file(img_new_path)  # 从新的路径获取图片
            # await msg.say(file_box_2)
            # return file_box_2
            text = file_box_2
        elif msg._payload.type == MessageType.MESSAGE_TYPE_AUDIO:
            file_box_audio = await msg.to_file_box()
            os.chmod(mp3_path, stat.S_IRWXU)
            comment_util.createFile(mp3_path)
            saved_file = os.path.join(mp3_path, file_box_audio.name)
            await file_box_audio.to_file(file_path=saved_file, overwrite=True)
            # # 将本地保存的语音文件发送给说话者
            # new_audio_file = FileBox.from_file(saved_file)
            # new_audio_file.metadata = {
            #     "voiceLength": 2000
            # }
            pcmPath=mp3_path+"\\"+file_box_audio.name.split(".")[0]+".pcm"
            target=mp3_path+"\\"+file_box_audio.name.split(".")[0]+".mp3"
            comment_util.voice_to_wav(saved_file,pcmPath=pcmPath,target=target)
            file_list=[]
            file_list.append(host_name+os.path.basename(target))
            text= paraformer_demo.ansyn_change_voice(file_list)
            # audio_path_new = resample_rate(saved_file, new_sample_rate=16000)  # 转换能识别格式
            # text = aip_asr(audio_path_new)  # 语音识别成文字
            # bot_response = model.predict(data=text)  # 生产文字回复
            # bot_response_path = aip_synthesis(bot_response, wav_path_res)  # 语音生成
            # file_box_audio_new = FileBox.from_file(bot_response_path)
            # await msg.say(file_box_audio_new)
        msg = dashscope_demo.call_with_messages(text)
        await conversation.say(msg)



import librosa
import os
import numpy as np
import soundfile as sf

async def resample_rate(path,new_sample_rate = 16000):
    signal, sr = librosa.load(path, sr=None)
    wavfile = path.split('/')[-1]
    wavfile = wavfile.split('.')[0]
    file_name = wavfile + '_new.wav'
    new_signal = librosa.resample(signal, sr, new_sample_rate) #
    #librosa.output.write_wav(file_name, new_signal , new_sample_rate)
    sf.write(file_name, new_signal, new_sample_rate, subtype='PCM_24')
    print(f'{file_name} has download.')
    return file_name




# async def choice_type(type, msg):
#     text=None
#
#     return text












bot: Optional[Wechaty] = None


async def main() -> None:
    """doc"""
    # pylint: disable=W0603
    global bot
    bot = Wechaty().on('message', message).use(plugin).use(plugin_msg)
    await bot.start()


asyncio.run(main())
