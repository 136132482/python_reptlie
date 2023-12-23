"""doc"""
import asyncio
import logging
from typing import Optional, Union

from wechaty_puppet import FileBox

from wechaty import Wechaty, Contact
from wechaty.user import Message, Room

from wechaty_bot   import  dashscope_demo
from wechaty_puppet import ContactType

import os
# os.environ['WECHATY_PUPPET_SERVICE_TOKEN']='puppet_padlocal_8016548d2b554ebbb4f5c89767a83b00'
# os.environ['WECHATY_PUPPET']='wechaty-puppet-padlocal'
os.environ['WECHATY_PUPPET_SERVICE_ENDPOINT']='192.168.0.107:7891'
os.environ['WECHATY_TOKEN']='968e1180-d977-4826-97fa-6784203d03c6'

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(filename)s <%(funcName)s> %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)

log = logging.getLogger(__name__)



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

bot: Optional[Wechaty] = None


async def main() -> None:
    """doc"""
    # pylint: disable=W0603
    global bot
    bot = Wechaty().on('message', message)
    await bot.start()


asyncio.run(main())
