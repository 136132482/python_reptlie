"""doc"""
import asyncio
import logging
from typing import Optional, Union,Dict

from wechaty_grpc.wechaty.puppet import MessageType
from wechaty_puppet import FileBox
from wechaty import Wechaty, Contact
from wechaty.user import Message, Room
from wechaty import Wechaty, MiniProgram
from wechaty_bot   import  dashscope_demo
from wechaty_puppet import ContactType
from wechaty_plugin_contrib.matchers import ContactMatcher


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

img_path='f:\\'
mp3_path=''


async def message(msg: Message) -> None:
    """back on message"""
    from_contact = msg.talker()
    text = msg.text()

    print(msg.to_file_box())
    print(text)
    room = msg.room()
    print(msg.type())
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
        msg = dashscope_demo.call_with_messages(text)
        await conversation.say(msg)


async def choice_type(type, msg):
    if type == MessageType.MESSAGE_TYPE_IMAGE:
        file_box_2 = await msg.to_file_box()
        # 将Message转换为FileBox
        await file_box_2.to_file(file_path=img_path, overwrite=True)  # 将图片保存为本地文件
        # img_new_path = img_transform(img_in_path)  # 调用图片风格转换的函数
        # file_box_3 = FileBox.from_file(img_new_path)  # 从新的路径获取图片
        # await msg.say(file_box_2)
        # return file_box_2

    elif type == MessageType.MESSAGE_TYPE_AUDIO:
            file_box_audio = await msg.to_file_box()
            await file_box_audio.to_file(file_path=mp3_path, overwrite=True)
            # audio_path_new = resample_rate(mp3_path, wav_path, new_sample_rate=16000)  # 转换能识别格式
            # text = aip_asr(audio_path_new)  # 语音识别成文字
            # bot_response = model.predict(data=text)  # 生产文字回复
            # bot_response_path = aip_synthesis(bot_response, wav_path_res)  # 语音生成
            # file_box_audio_new = FileBox.from_file(bot_response_path)
            # await msg.say(file_box_audio_new)














bot: Optional[Wechaty] = None


async def main() -> None:
    """doc"""
    # pylint: disable=W0603
    global bot
    bot = Wechaty().on('message', message).use(plugin).use(plugin_msg)
    await bot.start()


asyncio.run(main())
